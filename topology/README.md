# Topology — Network Analysis on PhosphoAtlas

Pre-GNN analysis exploring whether classical network-topology features on the PhosphoAtlas graph could distinguish tumor treatment groups on their own. The conclusion (network structure dominated over biological signal even when re-weighted) motivated the move to GNN-based feature learning.

## What's here

- `notebooks/Topology_Analysis_GNN.ipynb` — Spearman correlations between centrality and kinase activity, random-walk-with-restart (RWR), weighted RWR.

## Data

This module reads the same three files as `gnn/`. Symlink or copy them into `topology/data/` — see `data/README.md`.

> **Heads up:** the original notebook used absolute HPC paths (`/data/users/lima/*.xlsx`). They've been rewritten to relative `data/<filename>` paths so the notebook runs locally.

## How to run

```bash
jupyter notebook notebooks/Topology_Analysis_GNN.ipynb
```
