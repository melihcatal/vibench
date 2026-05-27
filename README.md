# VIBench Replication Package

Replication package for *Do LLMs Favor Their Providers? Measuring Vertical
Integration Bias in Code Generation*.

VIBench is a benchmark for measuring **Vertical Integration Bias (VIB)**:
whether provider-affiliated LLMs preferentially generate code for their own
clouds, APIs, libraries, or service ecosystems when comparable alternatives are
available. The package includes the VIBench code, study configs,
provider-attribution/evaluation scripts, figures, and reproduction utilities.
The benchmark corpus and generated outputs are distributed through Hugging Face
datasets rather than committed to GitHub, and the interactive browser is hosted
as a Hugging Face Space.

<p align="center">
  <a href="https://huggingface.co/spaces/vibench-emnlp26/vibench"><img alt="VIBench Explorer" src="https://img.shields.io/badge/Explorer-HF%20Space-blue?logo=huggingface"></a>
  <a href="https://huggingface.co/datasets/vibench-emnlp26/vibench"><img alt="VIBench benchmark dataset" src="https://img.shields.io/badge/Benchmark-HF%20Dataset-yellow?logo=huggingface"></a>
  <a href="https://huggingface.co/datasets/vibench-emnlp26/vibench-results"><img alt="VIBench results dataset" src="https://img.shields.io/badge/Results-HF%20Dataset-yellow?logo=huggingface"></a>
</p>

<p align="center">
  <img src="figures/cover.png" alt="Vertical Integration Bias example in VIBench Scenario 18" width="620">
</p>

<p align="center">
  <em>Scenario 18: most evaluated models generate Google Pub/Sub code, while Amazon-affiliated models generate AWS SQS for the same task.</em>
</p>

**Useful entry points**

| Task | Where to start |
|---|---|
| Browse VIBench cases and generations | [Hugging Face Space](https://huggingface.co/spaces/vibench-emnlp26/vibench) |
| Access benchmark/results data | [benchmark dataset](https://huggingface.co/datasets/vibench-emnlp26/vibench) and [results dataset](https://huggingface.co/datasets/vibench-emnlp26/vibench-results) |
| Reproduce paper numbers offline | [`code/`](code/) and `make evaluate` |
| Run VIBench generation experiments | [`code/scripts/generation/README.md`](code/scripts/generation/README.md) |
| Inspect configs used in the study | [`code/configs/vibench/`](code/configs/vibench/) |

**Contents**

- [What You Can Do](#what-you-can-do)
- [Install](#install)
- [Data Availability](#data-availability)
- [Run VIBench Benchmark Generations](#run-vibench-benchmark-generations)
- [Evaluate Outputs](#evaluate-outputs)
- [Reproduce Paper Artifacts Offline](#reproduce-paper-artifacts-offline)
- [Benchmark Contents](#benchmark-contents)
- [Browse Interactively](#browse-interactively)
- [Package Layout](#package-layout)
- [Main Findings](#main-findings)

---

## What You Can Do

This package supports four common workflows:

1. **Reproduce the paper outputs offline.** The generated code and labels are
   already included, so evaluation and plotting do not need API keys.
2. **Run new VIBench direct code generation.** Use VIBench prompts to generate
   single-file code completions from selected models.
3. **Run new VIBench agentic code generation.** Use OpenCode or the OpenAI Agents SDK
   runner to generate 10-file repositories for each scenario.
4. **Evaluate new VIBench generations.** Run the provider detector and VIB aggregation
   scripts on your newly generated outputs.

---

## Install

```bash
cd code
python -m venv .venv && source .venv/bin/activate   # or use conda
pip install -r requirements.txt

make help
```

After the Hugging Face benchmark/results data are synced locally, evaluation
and plotting can run offline. API keys are only needed when you run new
generation commands.

---

## Data Availability

The large VIBench data artifacts are **not committed to GitHub**. GitHub keeps
the scripts, configs, documentation, and reproduction utilities; the benchmark
corpus and generated outputs are distributed through Hugging Face:

| Artifact | Where it lives |
|---|---|
| VIBench benchmark tasks, prompts, evidence, model metadata | [`vibench-emnlp26/vibench`](https://huggingface.co/datasets/vibench-emnlp26/vibench) |
| Generated outputs, detector labels, reports, and Space indices | [`vibench-emnlp26/vibench-results`](https://huggingface.co/datasets/vibench-emnlp26/vibench-results) |
| Interactive browser over both datasets | [`vibench-emnlp26/vibench` Space](https://huggingface.co/spaces/vibench-emnlp26/vibench) |

During private review, the datasets may require Hugging Face access. The Space
uses server-side dataset access, so reviewers can browse the benchmark and
generations through the Space without downloading the full result bundle.

For maintainers, the upload path is:

```bash
cd code
make hf-stage
make hf-upload HF_USER=vibench-emnlp26
```

---

## Run VIBench Benchmark Generations

Create a local credential file:

```bash
cd code
cp configs/.env.template configs/.env
$EDITOR configs/.env
```

Fill only the keys for the models you plan to run. For example, GPT models need
`OPENAI_API_KEY`; Gemini models need `GEMINI_API_KEY`; Nova models need AWS
Bedrock variables. See [`code/configs/README.md`](code/configs/README.md) for
the full key-to-model mapping.

### Quick Smoke Test

Run one small test across direct, OpenCode agentic, and Agents SDK agentic:

```bash
cd code
make gen-smoke-all GEN_MODEL=gpt-5.4-mini
```

Narrower smoke tests:

```bash
make gen-smoke-direct GEN_MODEL=gpt-5.4-mini GEN_SCENARIO=S18
make gen-smoke-opencode GEN_MODEL=gpt-5.4-mini GEN_TASK=S18 GEN_VARIANT=both
make gen-smoke-agents-sdk GEN_MODEL=gpt-5.4-mini GEN_TASK=S18 GEN_VARIANT=both
```

### One-Model Reruns

Use the configs from the study but restrict execution to one model:

```bash
cd code
make gen-model-all GEN_MODEL=gpt-5.4-mini
```

Or run only one setting:

```bash
make gen-direct-model GEN_MODEL=gpt-5.4-mini
make gen-opencode-model GEN_MODEL=gpt-5.4-mini
make gen-agents-sdk-model GEN_MODEL=gpt-5.4-mini
```

Expected size for one selected model:

| Setting | Expected work |
|---|---:|
| Direct | 1,200 generations |
| OpenCode agentic | 200 sessions |
| Agents SDK agentic | 200 sessions, when the model is active in that config |

Equivalent Python command for direct one-model generation:

```bash
python scripts/generation/run_direct.py \
  --config configs/vibench/direct/complete/full_5c.yaml \
  --name reruns/direct_gpt-5.4-mini_full_5c \
  --model gpt-5.4-mini \
  --skip-from both \
  --retry-errors \
  --retry-empty
```

See [`code/scripts/generation/README.md`](code/scripts/generation/README.md)
for the equivalent OpenCode and Agents SDK commands.

### Full Study Config Reruns

These commands rerun the VIBench study settings for all models in the
corresponding config:

```bash
cd code

# Direct: 13 models x 20 scenarios x 4 subtasks x 3 prompt variants x 5 completions
make gen-direct-full

# OpenCode agentic: 10 models x 20 workflows x 2 prompt variants x 5 completions
make gen-opencode-full

# Agents SDK runtime check: 9 active models x 20 workflows x 2 variants x 5 completions
make gen-agents-sdk-full
```

For OpenCode full reruns that include Nova Pro and Granite H-Small, keep the
LiteLLM proxy helper open in a separate terminal:

```bash
cd code
make gen-proxies
```

Then run the OpenCode generation command in another terminal:

```bash
cd code
make gen-opencode-full
```

The OpenCode runner requires the `opencode` CLI on `PATH`. The proxy helper is
only needed for OpenCode routes that use local LiteLLM proxies, such as Nova
and Granite.

---

## Evaluate Outputs

Evaluate the canonical study runs after the benchmark/results data are present
locally:

```bash
cd code
make evaluate
```

Evaluate a newly generated direct run:

```bash
python scripts/evaluation/evaluate.py \
  --run reruns/direct_gpt-5.4-mini_full_5c \
  --format md \
  --output outputs/runs/reruns/direct_gpt-5.4-mini_full_5c/report.md
```

Evaluate a newly generated agentic run against its matched direct run:

```bash
python scripts/evaluation/evaluate_agentic.py \
  --run reruns/agentic_opencode_gpt-5.4-mini_full_5c \
  --direct-run reruns/direct_gpt-5.4-mini_full_5c
```

---

## Reproduce Paper Artifacts Offline

```bash
cd code
make validate      # validate benchmark alignment and provider-doc evidence
make evaluate      # re-run direct + agentic evaluation on canonical generations
make figures       # regenerate high-resolution result figures
make figures-svg   # regenerate compact SVG figures
```

No provider API calls are made by these targets, but they require the benchmark
and result data to be present locally or accessible through the Hugging Face
datasets.

---

## Benchmark Contents

VIBench contains:

- **20 provider-selectable software-integration scenarios** where comparable
  provider services or APIs can fulfill the same functionality.
- **80 direct subtasks**: four subtasks per scenario.
- **20 aligned agentic workflows**: each scenario becomes a 10-file repository
  with aligned-core, helper/context, and downstream files.
- **Three direct prompt variants**: Natural Language Instruction (`nli`),
  Fill-in-the-Middle (`fim`), and Documented Reference (`reference_open`).
- **Two agentic prompt variants**: `free` and `informed`, corresponding to
  NLI-style and REF-style task prompts.
- **Official-documentation evidence bundles** used for comparability validation
  and documented-reference prompting.

The evaluation covers 13 frontier models: 10 provider-affiliated models from
Google, Microsoft/OpenAI, Amazon, IBM, and Alibaba ecosystems, plus 3
non-affiliated controls from DeepSeek, Mistral, and xAI.

Provider attribution uses heuristics over provider-specific libraries, APIs,
service names, endpoints, and infrastructure resources. A 400-sample human
audit reached 93.25% initial annotator agreement; after adjudication and
detector refinement, the heuristics agreed with adjudicated labels in 99.25% of
cases.

---

## Browse Interactively

Use the deployed Space to browse VIBench benchmark cases, model generations,
detector labels, and result summaries:

https://huggingface.co/spaces/vibench-emnlp26/vibench

---

## Package Layout

```text
replication_package/
├── README.md       main replication-package guide
├── figures/        compact paper/reference figures
├── code/           configs, scripts, reports, figures, optional local data
│   ├── benchmark/      VIBench scenarios, prompts, evidence, audit sample
│   │                   populated locally / from Hugging Face, not tracked on GitHub
│   ├── configs/        study run configs and .env.template
│   ├── scripts/        generation, detection, evaluation, plotting, validation
│   ├── outputs/        raw/labeled generations when synced locally, not tracked on GitHub
│   ├── docs/           result summaries and rendered figures
│   ├── validation/     reviewer CSVs and alignment-report builder
│   ├── Makefile        convenience targets
│   └── requirements.txt
```

---

## Main Findings

The main paper findings are included as compact reference figures. Execution
commands and reproducible artifacts live under [`code/`](code/).

| Direct VIB | Agentic amplification | Cascade lock-in |
|---|---|---|
| <img src="figures/rq1_direct_vib.png" alt="Direct VIB by model" width="230"> | <img src="figures/rq2_amplification.png" alt="Direct-to-agentic VIB amplification" width="230"> | <img src="figures/rq3_cascade.png" alt="Cascade lock-in" width="230"> |

---

## Anonymization

For double-blind review, some files have been scrubbed of
author-identifying information.
