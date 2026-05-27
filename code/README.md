# VIBench — Code & Data

This folder contains the code-side core of the VIBench replication package:
scripts, configs, result reports, validation files, and the expected local
layout for benchmark/results data. See the [top-level README](../README.md) for
the research overview and findings.

Evaluation and plotting run **offline** once the Hugging Face benchmark/results
data have been synced into `code/benchmark/` and `code/outputs/`. Only
re-running the *generation* step needs live provider APIs.

**Contents**

- [Layout](#layout)
- [Install](#install)
- [Reproduce Offline](#reproduce-offline)
- [Re-running Generation](#re-running-generation-needs-api-keys)
- [Loading the Benchmark Programmatically](#loading-the-benchmark-programmatically)
- [Interactive Explorer](#interactive-explorer)
- [Notes](#notes)

## Layout

```text
code/
├── benchmark/vibench/   20 scenarios, direct + agentic task files, system prompts,
│                        models.json, provider-doc evidence snapshots, n=400 audit sample
├── configs/             run configs (direct/agentic) + .env.template (no secrets)
├── scripts/
│   ├── generation/      run_direct.py, run_agentic.py, run_agentic_litellm_agents.py
│   ├── evaluation/      detect_services.py, evaluate.py, evaluate_agentic.py, judges, tables
│   ├── plotting/        figure rendering
│   ├── benchmark/       benchmark construction + validation utilities
│   ├── audit/           detector audit-sample generation
│   ├── utils/           operational helpers (incl. optional HF upload staging)
│   └── vibench_loader.py  local-first dataset loader
├── outputs/runs/        raw + labeled generations, per-run config.yaml + report.md
├── outputs/audits/      human / LLM-judge audit artifacts
├── results/             pointer notes to the per-run reports
├── docs/                result summaries (docs/results) + rendered figures (docs/figures)
├── validation/          reviewer1.csv / reviewer2.csv + build_alignment_report.py
├── Makefile             convenience targets (make help)
└── requirements.txt
```

## Install

```bash
python -m venv .venv && source .venv/bin/activate   # or: conda create -n vibench python=3.11
pip install -r requirements.txt
```

## Reproduce (offline)

```bash
make help          # list targets
make figures       # regenerate high-res claude_*.png result charts into docs/figures
make figures-svg   # compact SVG overview / multi-label charts
make evaluate      # re-run direct + agentic evaluation on canonical runs
make validate      # validate benchmark alignment + provider-doc evidence
make audit-sample  # regenerate the seeded n=400 detector audit sample
```

The canonical runs used in the paper are:

- direct: `direct/complete/full_5c`
- agentic (OpenCode): `agentic/complete/opencode_full_5c`
- agentic (Agents SDK): `agentic/complete/agents_sdk_full_5c`

Evaluate them directly:

```bash
python scripts/evaluation/evaluate.py --run direct/complete/full_5c --format md \
  --output outputs/runs/direct/complete/full_5c/report.md
python scripts/evaluation/evaluate_agentic.py --run agentic/complete/opencode_full_5c \
  --direct-run direct/complete/full_5c
```

## Re-running generation (needs API keys)

Only required if you want to regenerate model outputs from scratch. Generation
is the only provider-API-dependent step; evaluation uses already-generated
outputs from the Hugging Face results bundle or local runs.

1. Create the local credential file:

   ```bash
   cp configs/.env.template configs/.env
   $EDITOR configs/.env
   ```

   The runners load `configs/.env` automatically. Fill only the keys for the
   models you run; see [configs/README.md](configs/README.md) for the exact
   key-to-model mapping.

2. Run a small smoke test before a full run. This example schedules one
   Gemini completion for each S18 direct subtask, so it makes four API calls:

   ```bash
   python scripts/generation/run_direct.py \
     --config configs/vibench/direct/complete/full_5c.yaml \
     --name scratch/direct_gemini_s18_nli \
     --model gemini-2.5-flash \
     --scenario S18 \
     --modality nli \
     --completions 1 \
     --sequential \
     -v
   ```

3. Run full direct generation into a new run directory. The study config
   schedules 15,600 calls: 13 models x 20 scenarios x 4 subtasks x 3 prompt
   variants x 5 completions.

   ```bash
   python scripts/generation/run_direct.py \
     --config configs/vibench/direct/complete/full_5c.yaml \
     --name reruns/direct_full_5c \
     --skip-from both \
     --retry-errors \
     --retry-empty
   ```

4. Run agentic generation. The study OpenCode config schedules 2,000
   sessions: 10 models x 20 workflows x 2 prompt variants x 5 completions.
   For this runtime, install the
   `opencode` CLI and keep the local LiteLLM proxy helper running in another
   terminal for Nova Pro and Granite H-Small:

   ```bash
   scripts/generation/start_litellm_proxies.sh
   ```

   Then run:

   ```bash
   python scripts/generation/run_agentic.py \
     --config configs/vibench/agentic/complete/opencode_full_5c.yaml \
     --name reruns/agentic_opencode_full_5c \
     --retry-errors \
     --retry-empty \
     --retry-incomplete
   ```

   The Agents SDK runtime check uses a separate runner and does not require the
   OpenCode CLI. Its study config has 9 active models and schedules 1,800
   sessions:

   ```bash
   python scripts/generation/run_agentic_litellm_agents.py \
     --config configs/vibench/agentic/complete/agents_sdk_full_5c.yaml \
     --name reruns/agentic_agents_sdk_full_5c \
     --retry-errors \
     --retry-empty \
     --retry-incomplete
   ```

5. Evaluate newly generated raw outputs:

   ```bash
   python scripts/evaluation/evaluate.py \
     --run reruns/direct_full_5c \
     --format md \
     --output outputs/runs/reruns/direct_full_5c/report.md

   python scripts/evaluation/evaluate_agentic.py \
     --run reruns/agentic_opencode_full_5c \
     --direct-run reruns/direct_full_5c
   ```

Use `--resume direct/complete/full_5c` or
`--resume agentic/complete/opencode_full_5c` only when you intentionally want to
continue or retry canonical study run directories. Full command details,
smoke tests, and ablation commands are in
[scripts/generation/README.md](scripts/generation/README.md).

The Makefile also exposes API-dependent generation wrappers. For example:

```bash
make gen-smoke-all GEN_MODEL=gpt-5.4-mini

# Study settings, filtered to one model
make gen-model-all GEN_MODEL=gpt-5.4-mini
make gen-direct-model GEN_MODEL=gpt-5.4-mini
make gen-opencode-model GEN_MODEL=gpt-5.4-mini
make gen-agents-sdk-model GEN_MODEL=gpt-5.4-mini

# Study settings, all configured models
make gen-direct-full
make gen-opencode-full     # run make gen-proxies first for Nova/Granite
make gen-agents-sdk-full
```

## Loading the benchmark programmatically

```python
import sys; sys.path.insert(0, "scripts")
from vibench_loader import load_benchmark, load_models, load_system_prompt

tasks  = load_benchmark(config="direct")    # local-first; offline by default
models = load_models()
prompt = load_system_prompt(prompt_type="agentic")
```

## Interactive explorer

Use the online VIBench Explorer to browse benchmark cases, model generations,
detector labels, and result summaries:

https://huggingface.co/spaces/vibench-emnlp26/vibench

The Space reads the Hugging Face benchmark and results datasets directly. This
replication package no longer ships an offline explorer copy.

## Notes

- GitHub does not track the large `code/benchmark/` and `code/outputs/`
  bundles. They are distributed through the Hugging Face datasets
  `vibench-emnlp26/vibench` and `vibench-emnlp26/vibench-results`; maintainers
  can refresh them with `make hf-stage` and `make hf-upload`.
- No secrets are included. `code/configs/.env.template` shows the expected
  variable names with dummy values.
