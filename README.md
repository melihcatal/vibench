# VIBench

Replication package for *Do LLMs Favor Their Providers? Measuring Vertical
Integration Bias in Code Generation*.

**Vertical Integration Bias (VIB)** measures whether a provider-affiliated LLM
selects its own provider's cloud services, APIs and libraries more often than
matched non-affiliated control models do on the same task. VIBench is the
benchmark: 20 software-integration scenarios in which a provider must be chosen
and comparable alternatives exist, evaluated both as single-file subtasks and as
ten-file agentic workflows.

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

## Contents

- [What ships here](#what-ships-here)
- [Install](#install)
- [Quickstart](#quickstart)
- [Working with the data](#working-with-the-data)
- [Running new generations](#running-new-generations)
- [Ablations](#ablations)
- [Benchmark contents](#benchmark-contents)
- [Layout](#layout)
- [Main findings](#main-findings)
- [Notes](#notes)

---

## What ships here


| | Where |
|---|---|
| Benchmark corpus — scenarios, tasks, prompts, model registry, audit sample | `code/benchmark/vibench/` |
| Generation, detection, evaluation, plotting code | `code/scripts/` |
| Study run configs | `code/configs/` |
| Generated code, detector labels, derived analysis tables | `outputs/` |
| Ablation runners and docs | `code/ablations/` |
| Ablation campaign runs | `outputs/ablations/` |
| Interactive browser over the same data | this repo, `code/explorer/` (`make explorer`), mirrored as a [Hugging Face Space](https://huggingface.co/spaces/vibench-emnlp26/vibench) |
| Provider-documentation snapshots | not shipped; rebuild with `make snapshots` |

**Note: API keys are needed only to generate new outputs.**

## Install

```bash
cd code
python -m venv .venv && source .venv/bin/activate
make install        # everything
make help
```

Most of this package needs **no third-party packages at all**: browsing the
benchmark, `make evaluate`, rebuilding the ablation tables and the annotator
validation report all run on the standard library. Install only what a task
adds:

| | Adds | For |
|---|---|---|
| *(nothing)* | — | browse, `make evaluate`, ablation tables, validation report |
| `make install-explorer` | Flask | `make explorer` |
| `make install-analysis` | numpy | `make gini-vib`, appendix tables, ablation evaluators |
| `make install-figures` | matplotlib, numpy | `make figures`, `make figures-svg` |
| `make install-generation` | litellm, openai-agents, python-dotenv, PyYAML, tqdm | producing new generations (also needs API keys) |
| `make install-hf` | huggingface_hub | reading the Hugging Face mirrors instead of this repo |

`requirements/` holds one file per row; `requirements.txt` is their union.

## Quickstart

Everything here reads the repository only.

**Look at the benchmark.**

```bash
make scenarios    # the 20 scenarios, and which ecosystems offer a service for each
make models       # the 13 study models and their provider affiliations
make runs         # which runs are present under outputs/
```

**Look at one generation**, and at what the detector made of it:

```bash
make browse ARGS="show --model nova-pro --scenario S18"
make browse ARGS="show --model nova-pro --scenario S04 --mode agentic"
```

**Compare models on the same task**, side by side:

```bash
make browse ARGS="compare --models affiliated --scenario S18"
make browse ARGS="compare --models gemini-2.5-flash,deepseek-v3.2 --scenario S18 --code"
```

**Or browse it all in a browser**, including every ablation:

```bash
make explorer          # http://127.0.0.1:8000
```

Ecosystems are colour-coded and each column says whether the model picked its
own ecosystem, a rival, or a neutral option, so one screen shows what the paper
measures. `python scripts/browse.py --help` lists every selector: subtask,
prompt variant, completion index, agentic session file, and run — including the
ablation runs, so the same view works on the option-order sweep. To load the
benchmark in your own code instead, see
[`code/README.md`](code/README.md#loading-the-benchmark-programmatically).

**Reproduce the VIB results.** This re-runs provider detection over the
generated code in `outputs/runs/` and writes the direct and agentic reports.
It takes a few minutes:

```bash
make evaluate
```

**Rebuild every ablation result table** from the recorded analysis snapshots:

```bash
python ablations/snapshots/make_summaries.py
python ablations/snapshots/make_paper_summaries.py
```

**Run the ablation protocol tests**, which check input construction, sampling,
and the staged-disclosure protocol:

```bash
python -m unittest ablations.shared.tests.test_inputs
python -m unittest ablations.agentic_mechanism.task_disclosure.tests.test_staged
```

## Working with the data

These run against the labeled outputs already in the repository, with no API
calls and no downloads:

```bash
cd code
make evaluate      # direct + agentic evaluation over the canonical runs
make figures       # high-resolution result charts
make figures-svg   # compact SVG charts
make gini-all      # provider Gini indices across all prompt settings
make gini-vib      # per-model Gini and VIB with bootstrap intervals
```

`make evaluate` re-runs provider detection over the generated code, which takes
a few minutes. Agentic evaluation also accepts the labeled per-session records
when the generations are absent — useful if you prune `outputs/runs/*/raw/` to
slim a checkout — and says on stdout which source it used; the aggregation is
identical either way.


## Running new generations

Generation is the only part that needs credentials.

```bash
cd code
make env                 # creates configs/.env from the template
$EDITOR configs/.env     # fill in only the keys you need
```

`make env` never overwrites an existing `configs/.env`, and that file is
gitignored.

Fill only the keys for the models you intend to run — GPT models need
`OPENAI_API_KEY`, Gemini models `GEMINI_API_KEY`, and so on.
[`code/configs/README.md`](code/configs/README.md) has the full key-to-model
mapping, and `python scripts/utils/runnable_models.py` prints which models your
current `.env` can actually run.

**Smoke test** one model across all three runners:

```bash
make gen-smoke-all GEN_MODEL=gpt-5.4-mini
```

**One model, full study configs** — 1,200 direct generations and 200 agentic
sessions per runner:

```bash
make gen-model-all GEN_MODEL=gpt-5.4-mini
```

**The full study**:

```bash
make gen-direct-full       # 13 models x 20 scenarios x 4 subtasks x 3 variants x 5 completions
make gen-opencode-full     # 10 models x 20 workflows x 2 variants x 5 completions
make gen-agents-sdk-full   # runtime-robustness arm, on the OpenAI Agents SDK
```

The OpenCode runner needs the `opencode` CLI on `PATH`. Nova and Granite routes
go through local LiteLLM proxies, so keep `make gen-proxies` running in another
terminal for those.

**Evaluate a new run.** `make baseline-build` packages the published control
runs so `--baseline` can score a single model without re-running them:

```bash
python scripts/evaluation/core/evaluate.py --run reruns/my_run --format md
make eval-model MODEL=gpt-5.4-mini
```

## Ablations

All ten ablations in the paper live in [`code/ablations/`](code/ablations/README.md), each
in its own directory stating the concern it answers, why it was run, and what it
showed. Four are campaigns with their own runners; six recompute VIB from the
main labeled runs using `code/scripts/evaluation/`.

| # | Ablation | Question it answers |
|---|---|---|
| 1 | [`initial_provider/assigned_as_code`](code/ablations/initial_provider/assigned_as_code/) | Is persistence just following whatever the first file used? |
| 2 | [`initial_provider/by_instruction`](code/ablations/initial_provider/by_instruction/) | Does VIB respond to an imposed external preference? |
| 3 | [`agentic_mechanism/single_shot_multifile`](code/ablations/agentic_mechanism/single_shot_multifile/) | Is the agentic gap caused by multi-file generation alone? |
| 4 | [`agentic_mechanism/task_disclosure`](code/ablations/agentic_mechanism/task_disclosure/) | Is persistence advance planning over the visible task list? |
| 5 | [`outputs/tables/agent_runtime`](outputs/tables/agent_runtime/) | Is the agentic result specific to one agent framework? |
| 6 | [`outputs/tables/control_composition`](outputs/tables/control_composition/) | Does the result depend on which controls are in the baseline? |
| 7 | [`outputs/tables/affiliation_definition`](outputs/tables/affiliation_definition/) | Do the GPT results depend on merging Microsoft and OpenAI? |
| 8 | [`outputs/tables/concentration_vs_affiliation`](outputs/tables/concentration_vs_affiliation/) | Is VIB just re-measuring provider concentration? |
| 9 | [`outputs/tables/prompt_format`](outputs/tables/prompt_format/) | Is the effect an artifact of one prompt wording? |
| 10 | [`outputs/tables/option_order`](outputs/tables/option_order/) | Is selection an artifact of option position in the prompt? |

## Benchmark contents

- **20 provider-selectable scenarios**, each with documented, functionally
  comparable alternatives from more than one provider.
- **80 direct subtasks** — four per scenario.
- **20 agentic workflows** — each scenario as a ten-file repository with
  aligned-core, helper and downstream files.
- **Three direct prompt variants**: natural-language instruction (`nli`),
  fill-in-the-middle (`fim`), documented reference (`reference_open`).
- **Two agentic prompt variants**: `free` and `informed`.
- **Provider-documentation evidence** used for comparability validation and for
  documented-reference prompting.

The study evaluates 13 models: 10 provider-affiliated, from the Google,
Microsoft/OpenAI, Amazon, IBM and Alibaba ecosystems, and 3 non-affiliated
controls from DeepSeek, Mistral and xAI. The registry carries extra entries for
alternative serving routes of those same models.

Provider attribution uses heuristics over provider-specific libraries, APIs,
service names, endpoints and infrastructure resources. A 400-sample human audit
reached 93.25% initial annotator agreement; after adjudication the heuristics
agreed with adjudicated labels in 99.25% of cases.

## Layout

```text
.
├── README.md
├── figures/              paper reference figures
├── code/
│   ├── README.md
│   ├── benchmark/        scenarios, tasks, prompts, model registry, audit sample
│   ├── configs/          study run configs and .env.template
│   ├── scripts/          generation, detection, evaluation, plotting, validation
│   ├── validation/       annotator CSVs and the alignment-report builder
│   ├── Makefile
│   ├── requirements.txt
│   └── ablations/        ablation runners and docs for the four campaigns
│       ├── README.md         index of all ten ablations
│       ├── initial_provider/     assigned_as_code/  by_instruction/
│       ├── agentic_mechanism/    single_shot_multifile/  task_disclosure/
│       ├── shared/           campaign launcher, runner, protocol tests
│       ├── paper_inputs/     the paper's archived prompts, per scenario
│       ├── anchor_files/     supplied A1 implementations
│       ├── snapshots/        analysis snapshots + the two result generators
│       └── diffs/            prompt diffs against the paper's config
└── outputs/
    ├── README.md
    ├── runs/             main study + option-order runs (raw/ + labeled/)
    ├── ablations/        ablation campaign runs, grouped like the code
    └── tables/           every ablation's derived tables, one directory each
```

## Main findings

| Direct VIB | Agentic amplification | Cascade lock-in |
|---|---|---|
| <img src="figures/rq1_direct_vib.png" alt="Direct VIB by model" width="230"> | <img src="figures/rq2_amplification.png" alt="Direct-to-agentic VIB amplification" width="230"> | <img src="figures/rq3_cascade.png" alt="Cascade lock-in" width="230"> |

VIB is a relative behavioral measure. A positive value means a model selected
its own provider's services more often than the matched controls did on the same
task. It is not evidence of intent, of a causal mechanism, or that the selected
service is technically worse.

## Notes

**Nova routing.** The paper's runs served the Nova models through AWS Bedrock via
a local LiteLLM proxy, since no first-party Nova API existed at the time. The
ablations were run after Amazon published its first-party Nova API and use that
route. The models are the same; only the serving route differs, and each run
manifest records which one was used.

**Browse interactively.** `make explorer` serves a local web app over the
benchmark cases, generations, detector labels and all ten ablations, reading the
repository with no network and no keys. The same views are online as a
[Hugging Face Space](https://huggingface.co/spaces/vibench-emnlp26/vibench),
backed by the mirrors. See
[`code/README.md`](code/README.md#interactive-explorer).

**AI Usage Disclaimer.** The repository was written with the assistance of LLMs.