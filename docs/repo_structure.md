# Repo structure

```
ucsf-radonc-practicum/
├── README.md
├── requirements.txt
├── environment.yml
├── .env.example
├── .gitignore
│
├── gnn/                              # Module 1: tumor classification GNN
│   ├── README.md
│   ├── notebooks/GNN_Tumors.ipynb
│   ├── src/gnn_figures.py
│   ├── figures/
│   │   ├── confusion_matrix.png
│   │   ├── tumor_embeddings_pca.png
│   │   └── kinase_saliency_top20.png
│   ├── docs/{methods,results}.md
│   └── data/README.md
│
├── topology/                         # Module 2: network topology / RWR
│   ├── README.md
│   ├── notebooks/Topology_Analysis_GNN.ipynb
│   └── data/README.md
│
├── phospho_pipeline/                 # Module 3: UniProt → LLM normalization
│   ├── README.md
│   ├── phospho/                      # importable package
│   │   ├── __init__.py
│   │   ├── uniprot.py
│   │   ├── llm_normalize.py
│   │   ├── phosphosite.py
│   │   ├── darkkinome_dataset.py
│   │   ├── darkkinome_io.py
│   │   ├── io.py
│   │   └── io_utils.py
│   ├── scripts/
│   │   ├── run_pipeline.py
│   │   ├── build_updated_ptm_dataset.py
│   │   └── build_darkkinome_ptm_dataset.py
│   ├── notebooks/
│   │   ├── LLM_general_pipeline_.ipynb
│   │   ├── UniProt_functions.ipynb
│   │   ├── phosphoatlas_eda.ipynb
│   │   └── dark_kinome_tester.ipynb
│   ├── d_kinases/
│   │   ├── dkinases.ipynb
│   │   ├── dkinases_multiclass.ipynb
│   │   └── dkinases_ptm_classifier.ipynb
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_uniprot.py
│   │   └── test_llm_normalize.py
│   └── data/README.md
│
├── agent_benchmark/                  # Module 4: Qwen agent benchmark
│   ├── README.md
│   ├── agent_runner.py
│   ├── live_tools.py
│   ├── run.py
│   ├── qwen_prompt_testing/
│   │   ├── agent_with_http.py
│   │   ├── run_kinases_known_atlas.py
│   │   ├── run_paper_informed.py
│   │   ├── run_pipeline_informed.py
│   │   ├── test_qwen_prompt.py
│   │   ├── kinases_known_atlas_prompt.txt
│   │   ├── paper_informed_prompt.txt
│   │   └── pipeline_informed_prompt.txt
│   ├── variants/
│   │   ├── run_log.json
│   │   ├── naive/run_log.json
│   │   ├── paper_informed/run_log.json
│   │   └── pipeline_informed/run_log.json
│   ├── notes/
│   │   ├── qwen_notes.txt
│   │   ├── 04_07_2026_report.md
│   │   └── todo.md
│   └── data/README.md
│
└── docs/
    └── repo_structure.md
```
