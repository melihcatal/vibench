# VIBench — Code & Data

This folder contains the code-side core of the VIBench replication package:
scripts, configs, result reports, validation files, and the expected local
layout for benchmark/results data. See the [top-level README](../README.md) for
the research overview and findings.

The benchmark corpus (`code/benchmark/vibench/` — tasks, system prompts,
`models.json`, evidence source files, the n=400 audit sample) is tracked
directly in this repository. Evaluation and plotting run **offline** once the
generated outputs are present in `../outputs/`. Only
re-running the *generation* step needs live provider APIs.

**Contents**

- [Layout](#layout)
- [Install](#install)
- [Browse](#browse)
- [Reproduce Offline](#reproduce-offline)
- [Re-running Generation](#re-running-generation-needs-api-keys)
- [Loading the Benchmark Programmatically](#loading-the-benchmark-programmatically)
- [Interactive Explorer](#interactive-explorer)
- [Notes](#notes)

## Layout

```text
code/
├── benchmark/vibench/   20 scenarios, direct + agentic task files, system prompts,
│                        models.json, provider-doc evidence, n=400 audit sample
├── configs/             run configs (direct/agentic) + .env.template (no secrets)
├── scripts/
│   ├── generation/      run_direct.py, run_agentic.py, run_agentic_litellm_agents.py
│   ├── evaluation/      core/ detection + scoring, plus gini/, tables/, baselines/, audit/
│   ├── plotting/        figure rendering
│   ├── benchmark/       benchmark construction + validation utilities
│   ├── audit/           detector audit-sample generation
│   ├── utils/           model registry helpers and route checks
│   ├── browse.py        read the benchmark and the generations from the terminal
│   └── vibench_loader.py  local-first dataset loader
├── ablations/           ablation runners and docs — see ablations/README.md
├── explorer/            offline web explorer (make explorer)
├── validation/          reviewer1.csv / reviewer2.csv + build_alignment_report.py
├── Makefile             convenience targets (make help)
├── requirements/        one file per install option
└── requirements.txt
```

Generated data lives outside this directory, in `../outputs/`: `runs/` holds the
raw and labeled generations, `ablations/` the campaign runs, and `control_sets/`
the packaged control outputs. `make figures` writes into `docs/figures/` here,
and `make gini-*` into `../outputs/tables/`; both are created on demand.

## Install

```bash
python -m venv .venv && source .venv/bin/activate   # or: conda create -n vibench python=3.11
make install        # everything
```

Reading the shipped results needs no third-party packages: browsing, `make
evaluate`, the ablation table generators and the validation report all run on
the standard library. The smaller installs each add one thing:

```bash
make install-explorer     # Flask           -> make explorer
make install-analysis     # numpy           -> gini/appendix tables, ablation evaluators
make install-figures      # matplotlib      -> make figures, make figures-svg
make install-generation   # API clients     -> new generations (needs keys too)
make install-hf           # huggingface_hub -> read the HF mirrors
```

Each corresponds to a file in `requirements/`; `requirements.txt` is the union
of all five.

## Browse

`scripts/browse.py` reads the benchmark and the generated outputs in the
terminal. Ecosystems are colour-coded, and `compare` says per model whether it
picked its own ecosystem, a rival, or a neutral option.

```bash
make scenarios     # the 20 scenarios and the ecosystems eligible for each
make models        # the study models and their affiliations
make runs          # the runs present under ../outputs/runs/

make browse ARGS="scenario S18 --prompts"
make browse ARGS="show --model nova-pro --scenario S18"
make browse ARGS="show --model nova-pro --scenario S04 --mode agentic --file speech_client.py"
make browse ARGS="compare --models affiliated --scenario S18"
make browse ARGS="compare --models gemini-2.5-flash,deepseek-v3.2 --scenario S18 --code"
```

Selectors: `--subtask` (letter, number, or role name), `--prompt`
(`nli`/`fim`/`reference_open`, or `free`/`informed` with `--mode agentic`),
`--completion`, and `--run` for any run that `make runs` lists, ablations
included. `python scripts/browse.py --help` has the full list.

## Reproduce (offline)

```bash
make help          # list targets
make figures       # regenerate high-res claude_*.png result charts into docs/figures
make figures-svg   # compact SVG overview / multi-label charts
make evaluate      # re-run direct + agentic evaluation on canonical runs
make validate      # validate benchmark alignment + provider-doc evidence
make audit-sample  # draw a fresh n=400 detector audit sample into ../outputs/audits/
```

The canonical runs used in the paper are:

- direct: `direct/complete/full_5c`
- agentic (OpenCode): `agentic/complete/opencode_full_5c`
- agentic (Agents SDK): `agentic/complete/agents_sdk_full_5c`

Evaluate them directly:

```bash
python scripts/evaluation/core/evaluate.py --run direct/complete/full_5c --format md \
  --output ../outputs/runs/direct/complete/full_5c/report.md
python scripts/evaluation/core/evaluate_agentic.py --run agentic/complete/opencode_full_5c \
  --direct-run direct/complete/full_5c
```

## Re-running generation (needs API keys)

Only required if you want to regenerate model outputs from scratch. Generation
is the only provider-API-dependent step; evaluation uses already-generated
outputs from the Hugging Face results bundle or local runs.

1. Create the local credential file:

   ```bash
   make env                 # copies configs/.env.template, refusing to clobber
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
   python scripts/evaluation/core/evaluate.py \
     --run reruns/direct_full_5c \
     --format md \
     --output ../outputs/runs/reruns/direct_full_5c/report.md

   python scripts/evaluation/core/evaluate_agentic.py \
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

`explorer/` is a local web app over the same data — benchmark cases, model
generations, detector labels, and the ablations with their derived tables. It
reads the repository, so it needs no network and no keys:

```bash
make explorer                      # http://127.0.0.1:8000
make explorer EXPLORER_PORT=8900   # another port
```

Four views: **Benchmark Explorer** (scenarios, prompts, provider evidence),
**Results Summary** (totals and VIB, computed from the shipped runs),
**Ablations** (all ten: the concern each answers, its passes and coverage, and
its result tables), and **Result Evaluator** (filter generations by run, model,
scenario, subtask and prompt variant).

Every run is browsable in the Result Evaluator, including the ablations. The
run dropdown lists them in groups — the main runs, the option-order variants,
and the four generation campaigns — and each ablation's **open** button jumps
there with that run selected. The campaigns keep their own layout under
`../outputs/ablations/` (a cell per scenario x model x condition x repetition,
each with a generated repository and per-file detector labels), so they are
adapted into the same records the agentic sessions use: pick the `Ablation
cell` modality to see them, with the condition shown per record and every
generated file's source and provider label in the detail pane.

Each cell also shows the order its files were produced in, which is what the
persistence claims rest on. Where that order came from is labelled: the
agent-driven campaigns record every tool call with a timestamp in
`trace.json`, staged disclosure keeps its own per-step event list, and
single-shot generation has no recorded sequence at all — there the order is
marked *inferred*, being the order the files appear in one response.

It is read-only over the shipped data. The detector audit and the annotator
validation review are not part of it: those are labelling workflows rather than
things to browse, and they run as scripts — `make validate` builds the
annotator-agreement report from `validation/reviewer{1,2}.csv`, and
`make audit-sample` draws a fresh sample.

Nothing in it is hardcoded: record counts and VIB come from `outputs/`, so a
pruned or extended checkout reports its own contents. `make evaluate` first if
you want the Results Summary to reflect a re-run.

The same data is also browsable online, backed by the Hugging Face mirrors:

https://huggingface.co/spaces/vibench-emnlp26/vibench

To point the local app at those mirrors instead of the repository:

```bash
make explorer EXPLORER_ARGS="--benchmark-source hf --results-source hf"
```

## Notes

- The benchmark corpus is tracked in-repo except for two regenerable
  evidence artifacts (`evidence/generated/`, `evidence/snapshots/` — rebuild
  with `make snapshots`). The `../outputs/` run bundles are tracked here too,
  so nothing has to be downloaded; the Hugging Face datasets
  `vibench-emnlp26/vibench` (benchmark, flat export) and
  `vibench-emnlp26/vibench-results` (all runs) mirror the same data.
- No secrets are included. `code/configs/.env.template` shows the expected
  variable names with dummy values.
