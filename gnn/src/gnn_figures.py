"""
Plotting helpers for the Tumor GNN classification results.

Figures auto-save to FIGURES_DIR (default: ./figures/<filename>.png) unless
you pass save_path=False to disable or save_path="custom/path.png" to override.

Usage (inside the notebook, after results are computed):

    from gnn_figures import (
        plot_confusion_matrix,
        plot_top_kinase_saliency,
        plot_tumor_embeddings,
    )

    plot_confusion_matrix(results_loocv["y_true"], results_loocv["y_pred"])
    plot_top_kinase_saliency(rank_df_kinase, top_n=20)
    plot_tumor_embeddings(final_model, dataset_denoised, device)
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import torch.nn.functional as F
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix
from torch_geometric.nn import global_mean_pool


FIGURES_DIR = Path("figures")


def _resolve_save_path(save_path, default_filename):
    """
    Decide where to save a figure.
      - save_path=None        -> FIGURES_DIR/<default_filename>  (auto-save)
      - save_path=False       -> do not save
      - save_path="x.png"     -> save exactly there
    Ensures the parent directory exists.
    """
    if save_path is False:
        return None
    if save_path is None:
        save_path = FIGURES_DIR / default_filename
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    return save_path


def plot_confusion_matrix(
    y_true,
    y_pred,
    class_names=("UNT", "ENC+PAN"),
    figsize=(5.5, 4.5),
    title="LOOCV Classification Performance",
    save_path=None,
):
    """Confusion matrix heatmap annotated with counts and row-normalized percentages."""
    cm = confusion_matrix(y_true, y_pred)
    cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)

    annot = np.empty_like(cm).astype(object)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            annot[i, j] = f"{cm[i, j]}\n({cm_norm[i, j] * 100:.1f}%)"

    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        cm,
        annot=annot,
        fmt="",
        cmap="Blues",
        cbar=False,
        xticklabels=class_names,
        yticklabels=class_names,
        annot_kws={"size": 13, "weight": "bold"},
        linewidths=0.5,
        linecolor="white",
        ax=ax,
    )
    ax.set_xlabel("Predicted label", fontsize=12, fontweight="bold")
    ax.set_ylabel("True label", fontsize=12, fontweight="bold")
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()

    out = _resolve_save_path(save_path, "confusion_matrix.png")
    if out is not None:
        plt.savefig(out, dpi=300, bbox_inches="tight")
        print(f"Saved: {out}")
    plt.show()
    return fig


def plot_top_kinase_saliency(
    rank_df,
    top_n=20,
    gene_col="gene",
    score_col="score_grad_saliency",
    figsize=(6.5, 7),
    title="Top kinases by gradient saliency",
    save_path=None,
):
    """Horizontal bar chart of the top-N kinases ranked by saliency score."""
    top = rank_df.head(top_n).iloc[::-1]  # reverse so largest is on top

    fig, ax = plt.subplots(figsize=figsize)
    norm = plt.Normalize(top[score_col].min(), top[score_col].max())
    colors = plt.cm.viridis(norm(top[score_col].values))

    ax.barh(top[gene_col], top[score_col], color=colors, edgecolor="white")
    ax.set_xlabel("Gradient saliency  (|∂L / ∂activity|)", fontsize=11, fontweight="bold")
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="y", labelsize=10)
    plt.tight_layout()

    out = _resolve_save_path(save_path, f"kinase_saliency_top{top_n}.png")
    if out is not None:
        plt.savefig(out, dpi=300, bbox_inches="tight")
        print(f"Saved: {out}")
    plt.show()
    return fig


@torch.no_grad()
def _extract_pooled_embeddings(model, dataset, device):
    """Run the trained GNN's forward pass up to (and including) global mean pool."""
    model.eval()
    embeddings, labels, names = [], [], []
    for data in dataset:
        data = data.to(device)
        batch = (
            data.batch
            if getattr(data, "batch", None) is not None
            else torch.zeros(data.x.size(0), dtype=torch.long, device=device)
        )
        x = model.conv1(data.x, data.edge_index)
        x = F.relu(x)
        z = global_mean_pool(x, batch)  # (1, hidden_dim)
        embeddings.append(z.cpu().numpy().squeeze(0))
        labels.append(int(data.y.item()))
        names.append(getattr(data, "sample_name", ""))
    return np.array(embeddings), np.array(labels), names


def plot_tumor_embeddings(
    model,
    dataset,
    device,
    class_names=("UNT", "ENC+PAN"),
    figsize=(6.5, 5.5),
    title="Tumor embeddings (PCA of pooled GNN representation)",
    annotate=False,
    save_path=None,
):
    """PCA projection of the pooled GNN embedding for each tumor, colored by treatment class."""
    Z, y, names = _extract_pooled_embeddings(model, dataset, device)
    Z2 = PCA(n_components=2, random_state=0).fit_transform(Z)

    fig, ax = plt.subplots(figsize=figsize)
    palette = {0: "#4A90D9", 1: "#E8554E"}
    for cls, label in enumerate(class_names):
        mask = y == cls
        ax.scatter(
            Z2[mask, 0], Z2[mask, 1],
            s=90, alpha=0.85,
            color=palette[cls], edgecolor="white", linewidth=1.2,
            label=label,
        )
    if annotate:
        for (xc, yc, name) in zip(Z2[:, 0], Z2[:, 1], names):
            ax.annotate(name, (xc, yc), fontsize=7, alpha=0.6)

    ax.set_xlabel("PC1", fontsize=11, fontweight="bold")
    ax.set_ylabel("PC2", fontsize=11, fontweight="bold")
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.legend(title="Treatment", frameon=False, loc="best")
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()

    out = _resolve_save_path(save_path, "tumor_embeddings_pca.png")
    if out is not None:
        plt.savefig(out, dpi=300, bbox_inches="tight")
        print(f"Saved: {out}")
    plt.show()
    return fig
