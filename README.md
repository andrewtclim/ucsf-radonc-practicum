# UCSF RadOnc Practicum

Computational biology and ML research on kinase signaling networks, conducted with UCSF Radiation Oncology. The project applies graph methods, LLM agents, and data-engineering pipelines to the PhosphoAtlas kinase–substrate map.

## Modules

| Module | What it does |
|---|---|
| [`gnn/`](./gnn) | Graph neural network classifying tumor treatment groups (UNT vs ENC+PAN) from HT-KAM kinase activity profiles, and ranking the kinases that drive the prediction. |
| [`topology/`](./topology) | Pre-GNN topology analysis on the PhosphoAtlas graph — centrality, Spearman correlations, random-walk-with-restart. |
| [`phospho_pipeline/`](./phospho_pipeline) | Data engineering pipeline that fetches UniProt PTM text and normalizes it into structured kinase–substrate records via an LLM, building a weakly supervised dataset for dark-kinome identification. |
| [`agent_benchmark/`](./agent_benchmark) | LLM agent benchmark: Qwen3-235B autonomously reconstructing the PhosphoAtlas, scored against the PA2 gold standard. Three prompt variants (naive, paper-informed, pipeline-informed). |

## Repo structure

```
ucsf-radonc-practicum/
├── README.md
├── requirements.txt              # pip
├── environment.yml               # conda alternative (recommended for torch-geometric)
├── .env.example                  # template for API keys
├── .gitignore                    # data/ blanket-excluded; whitelist what is safe
│
├── gnn/                          # Module 1
│   ├── notebooks/GNN_Tumors.ipynb
│   ├── src/gnn_figures.py
│   ├── figures/                  # confusion matrix, PCA, saliency
│   ├── docs/{methods,results}.md
│   └── data/README.md            # stub — private data, see module README
│
├── topology/                     # Module 2
│   ├── notebooks/Topology_Analysis_GNN.ipynb
│   └── data/README.md
│
├── phospho_pipeline/             # Module 3
│   ├── phospho/                  # importable package
│   ├── scripts/                  # run_pipeline.py and dataset builders
│   ├── notebooks/                # exploration / EDA
│   ├── d_kinases/                # dark-kinome classifier notebooks
│   ├── tests/                    # pytest
│   └── data/README.md
│
├── agent_benchmark/              # Module 4
│   ├── agent_runner.py, live_tools.py, run.py
│   ├── qwen_prompt_testing/      # prompt variants + tests
│   ├── variants/{naive,paper_informed,pipeline_informed}/  # run logs (atlas.json gitignored)
│   ├── notes/                    # qwen_notes, report, todo
│   └── data/README.md
│
└── docs/
    └── repo_structure.md
```

## Setup

### Option A — conda (recommended)

`torch-geometric` is dependency-heavy on pip; conda resolves it cleanly.

```bash
conda env create -f environment.yml
conda activate ucsf-radonc-practicum
cp .env.example .env  # then fill in API keys
```

### Option B — pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then fill in API keys
```

### API keys

Modules 3 and 4 hit external LLM APIs. Required env vars (see `.env.example`):

- `VERSA_API_KEY`, `AZURE_OPENAI_*` — for `phospho_pipeline` (UCSF Versa gateway → Azure OpenAI)
- `TOGETHER_API_KEY` — for `agent_benchmark` (Qwen3-235B via Together AI)

`gnn` and `topology` do not require API keys.

## Data

Most datasets are private (patient-derived, unpublished, or third-party-licensed) and are **not** included in the repo. Each module has a `data/README.md` listing the expected files and how to obtain them.

The full blanket exclusion is in `.gitignore`: every `data/` directory is ignored except for `README.md` files inside them.

## Running each module

See the per-module README. Quick pointers:

- `gnn/notebooks/GNN_Tumors.ipynb` — open in Jupyter, run top-to-bottom once data is in `gnn/data/`.
- `topology/notebooks/Topology_Analysis_GNN.ipynb` — same.
- `phospho_pipeline/`: `python -m phospho_pipeline.scripts.run_pipeline` or `pytest phospho_pipeline/tests/`.
- `agent_benchmark/`: `python agent_benchmark/run.py` (requires upstream dependency — see module README).
