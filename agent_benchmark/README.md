# Agent Benchmark — Qwen3-235B on PhosphoAtlas Reconstruction

LLM agent benchmark: can Qwen3-235B autonomously reconstruct the PhosphoAtlas kinase–substrate map from public sources? Three prompt variants tested:

- **naive** — minimal prompt, agent figures out the task from scratch
- **paper-informed** — prompt includes a summary of the PhosphoAtlas methods paper
- **pipeline-informed** — prompt includes the structured pipeline steps used by the human curators

Scored against PA2 gold standard (15,640 triples, 436 kinases) on precision, recall, F1, kinase discovery, and peptide accuracy.

## Relationship to the upstream repo

This module is a **contribution** to a sister repo, **`agent-pa-benchmark`** (UCSF RadOnc), and depends on infrastructure it does not vendor. Specifically, `agent_runner.py` and `live_tools.py` import:

```python
from agents.base_agent import BaseAgent          # upstream
from databases.tools import DatabaseTools        # upstream
```

To actually run the agent, the standard workflow is:

1. Clone the upstream `agent-pa-benchmark` repo.
2. Drop this folder under `contributions/andrew_qwen3_235b/` in that repo.
3. Run from the upstream root: `python contributions/andrew_qwen3_235b/run.py`.

The code is included here as a self-contained record of the contribution, prompts, run logs, and notes — not as a standalone runnable.

## What's here

- `agent_runner.py` — `QwenAgent` subclass of upstream `BaseAgent`; tool-call loop, entry accumulator, token tracking.
- `live_tools.py` — UniProt-fetch + PSP-lookup tools the agent can call.
- `run.py` — CLI entry: variant selection, output writing.
- `qwen_prompt_testing/` — the three prompt variants, prompt-test scripts.
- `variants/{naive,paper_informed,pipeline_informed}/run_log.json` — per-variant run logs.
  > `atlas.json` outputs are large (~5 MB each) and **gitignored**. Regenerate by re-running.
- `notes/qwen_notes.txt`, `notes/04_07_2026_report.md`, `notes/todo.md` — context and methods notes.

## API

Requires `TOGETHER_API_KEY` (Together AI). See `../.env.example`.

## Headline observations

See `notes/04_07_2026_report.md` for the writeup. Short version: prompt informedness matters more than scale; pipeline-informed beats paper-informed beats naive.
