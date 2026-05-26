# d_kinases — Dark-Kinome PTM Classifier

Notebooks training a multiclass classifier on the LLM-normalized PTM dataset to flag dark-kinome candidates.

## Notebooks

- `dkinases.ipynb` — initial exploration
- `dkinases_multiclass.ipynb` — multiclass classifier (kinase family)
- `dkinases_ptm_classifier.ipynb` — refined classifier with curated PTM features

## Inputs

These notebooks read `data_aq_ambig.csv` and the LLM-derived `updated_PTM_dataset_<date>.csv`. Both are produced by `phospho_pipeline/scripts/` and live in `phospho_pipeline/data/` — see that folder's README.
