# GNN — data

This folder is gitignored except for this README. Place the following files here before running `notebooks/GNN_Tumors.ipynb`:

| File | Description | Source |
|---|---|---|
| `2024_PhosphoAtlas 2.0_updated KSP network_withHTKAMconnections.xlsx` | Kinase–substrate network (14,043 edges, 2,944 genes) | PhosphoAtlas 2.0 — UCSF lab (not yet public; contact PI) |
| `BRAF_CDK_kinase profile_202500827_JPC2MBetAL_v01.csv` | Treatment labels and tumor volumes per sample | **Private** — UCSF, patient-derived, request through PI |
| `TumorSample_normalizedKinaseActivities_2025.xlsx` | Tumor × kinase activity matrix (44 samples × 192 kinases) | **Private** — UCSF, unpublished, request through PI |

The notebook reads them with relative paths (`data/<filename>`). If you obtain different filenames, update the path variables at the top of the notebook.
