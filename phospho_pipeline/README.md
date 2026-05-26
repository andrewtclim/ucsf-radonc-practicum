# Phosphorylation Pipeline

Data engineering pipeline that turns unstructured UniProt PTM annotations into a structured, weakly supervised kinase–substrate dataset for dark-kinome research.

## Pipeline shape

```
UniProt PTM text
   │
   ▼
phospho.uniprot       fetch + parse PTM records
   │
   ▼
phospho.llm_normalize LLM (UCSF Versa → Azure OpenAI) extracts {kinase, substrate, site}
   │
   ▼
phospho.phosphosite   validation, normalization, site formatting
   │
   ▼
updated_PTM_dataset.csv     (weakly supervised dataset)
```

## What's here

- `phospho/` — importable package
  - `uniprot.py` — UniProt search/fetch + parsing helpers
  - `llm_normalize.py` — LLM client (reads `VERSA_API_KEY` from env) + normalization
  - `phosphosite.py` — site validation and formatting
  - `darkkinome_dataset.py`, `darkkinome_io.py` — dark-kinome–specific dataset builders
  - `io.py`, `io_utils.py` — run directory and write helpers
- `scripts/`
  - `run_pipeline.py` — full UniProt → LLM pipeline
  - `build_updated_ptm_dataset.py` — dataset assembly
  - `build_darkkinome_ptm_dataset.py` — dark-kinome variant
- `notebooks/` — exploratory: EDA, UniProt API exploration, smoke tests
- `d_kinases/` — dark-kinome multiclass classifier notebooks (consumes the pipeline's output)
- `tests/` — pytest unit tests for `uniprot.py` and `llm_normalize.py`

## Setup

```bash
cp ../.env.example ../.env   # fill in VERSA_API_KEY and AZURE_OPENAI_*
```

## How to run

```bash
# unit tests
pytest tests/

# full pipeline
python scripts/run_pipeline.py
```

## Data

See `data/README.md`. The PhosphoAtlas xlsx and Dark Kinome KB CSVs are gitignored; LLM-derived outputs go to `data/` and are also gitignored.
