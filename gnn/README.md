# GNN — Tumor Classification and Kinase Ranking

Graph neural network that classifies tumor treatment groups (UNT vs ENC+PAN) from HT-KAM kinase activity profiles, then ranks the kinases driving the classification.

## What's here

- `notebooks/GNN_Tumors.ipynb` — full pipeline: graph construction, denoising autoencoder, GNN training (LOOCV), saliency.
- `src/gnn_figures.py` — figure generation helpers (confusion matrix, PCA, saliency bar chart).
- `figures/` — published figures (PNG).
- `docs/methods.md`, `docs/results.md` — methods text and results narrative.

## Pipeline (3 stages)

1. **Graph construction** — directed kinase→substrate graph from PhosphoAtlas (14,043 edges, 2,944 nodes). Node features per tumor: `[kinase activity, in-degree, out-degree, in-degree centrality]`.
2. **Denoising autoencoder (`TumorAE`)** — compresses the 192-dim kinase activity vector through a 16-dim bottleneck, trained 300 epochs with MSE. Denoised profiles replace raw activity in the GNN's node features and lift LOOCV accuracy from ~54% to ~91%.
3. **GNN** — `TumorGNN_Tiny` (1-layer GCN + global mean pool + linear head) for binary classification; evaluated via LOOCV due to n=44. `TumorGNN_Reg` (2-layer GCN + MLP head) for volume regression — unstable.

## Headline results

- LOOCV classification accuracy: **91%** with denoised features.
- Top predictive kinases (gradient saliency): PRKACA, PRKCA, CSNK2A1, CDK1, CDK2, ATM, SRC.

## Data

The data files are **private** (patient-derived, unpublished). See `data/README.md` for the expected file list and how to obtain access.

## How to run

```bash
conda activate ucsf-radonc-practicum   # or your venv
jupyter notebook notebooks/GNN_Tumors.ipynb
```

The notebook expects three files inside `gnn/data/` — see `data/README.md`.
