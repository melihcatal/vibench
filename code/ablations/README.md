# Ablations and robustness analyses

Every ablation in the paper, grouped by the question it answers. Each has its
own directory with a README stating the concern, why it was run, and what it
showed.

Two kinds. **Campaigns** have their own runners, configs, inputs and tests, and
live here. **Pipeline analyses** have no runner of their own: they recompute VIB
from the main labeled runs, and their scripts live in
`code/scripts/evaluation/tables/` and `/gini/` rather than here, because several
of them share helpers — the affiliation-sensitivity analysis imports from the
concentration one — so per-ablation folders would make one ablation import from
another.

Every ablation's derived tables, campaign or analysis, are in
`outputs/tables/<ablation>/`.

| # | Ablation | Question it answers | Paper |
|---|---|---|---|
| 1 | [`initial_provider/assigned_as_code`](initial_provider/assigned_as_code/) | Is persistence just following whatever the first file used? | new |
| 2 | [`initial_provider/by_instruction`](initial_provider/by_instruction/) | Does VIB respond to an imposed external preference? | new |
| 3 | [`agentic_mechanism/single_shot_multifile`](agentic_mechanism/single_shot_multifile/) | Is the agentic gap caused by multi-file generation alone? | new |
| 4 | [`agentic_mechanism/task_disclosure`](agentic_mechanism/task_disclosure/) | Is persistence advance planning over the visible task list? | new |
| 5 | [`outputs/tables/agent_runtime`](../../outputs/tables/agent_runtime/) | Is the agentic result specific to one agent framework? | Table 12 |
| 6 | [`outputs/tables/control_composition`](../../outputs/tables/control_composition/) | Does the result depend on which controls are in the baseline? | Table 14 |
| 7 | [`outputs/tables/affiliation_definition`](../../outputs/tables/affiliation_definition/) | Do the GPT results depend on merging Microsoft and OpenAI? | Table 15 |
| 8 | [`outputs/tables/concentration_vs_affiliation`](../../outputs/tables/concentration_vs_affiliation/) | Is VIB just re-measuring provider concentration? | Table 13 |
| 9 | [`outputs/tables/prompt_format`](../../outputs/tables/prompt_format/) | Is the effect an artifact of one prompt wording? | Table 9 |
| 10 | [`outputs/tables/option_order`](../../outputs/tables/option_order/) | Is selection an artifact of option position in the prompt? | Tables 10–11 |

Every campaign records a `code_sha256` map over the main runners, `models.json`
and both paper configs into its run manifest (`shared/campaign.py`), so each run
is tied to the exact code and design it ran against. `diffs/` holds unified
diffs between each campaign's prompts and the paper's originals, showing that
each changes exactly one thing.

---

## 1. Initial provider — assigned as code

**Concern.** Downstream provider choices might simply follow whatever the first
file already used, making persistence an artifact of the anchor rather than
affiliation.

**Why.** Supply the initial file (A1) as existing provider-specific code, vary
its provider, and leave the four downstream tasks unchanged. If persistence
were purely anchor-following, retention would not depend on whose anchor it is.

**Result.** Models follow the supplied anchor in 59.6% of downstream files
[53.7, 65.4], but retention is 28.0 pp higher when the anchor matches the
model's own affiliation [21.9, 34.2] — 78.2% for an own-ecosystem anchor versus
50.2% for a competing one.

## 2. Initial provider — assigned by instruction

**Concern.** VIB should respond to a controlled change in preference. If it does
not, the metric may not measure what it claims to.

**Why.** Instruct the model to implement the initial file with a named external
provider, then observe downstream choices. Unlike campaign 1 the anchor is
requested rather than supplied as code.

**Result.** Instructions are followed in 64.5% of downstream files [59.8, 69.3],
again 20.0 pp more often when the instructed provider matches the model's own
affiliation [14.4, 25.8]. The metric moves under imposed preference.

## 3. Agentic mechanism — single-shot multi-file generation

**Concern.** The agentic amplification result might come from agent tooling or
runtime behaviour rather than from multi-file generation itself.

**Why.** Generate the same ten-file task in one response, without agent tools,
and compare the affiliated share in task-aligned core files.

**Result.** The affiliated share is lower without agent tools for all three
models: 43.2% versus 79.0% (Gemini 2.5 Flash), 37.9% versus 43.5%
(GPT-5.4 Mini), 23.2% versus 70.0% (Nova Pro).

## 4. Agentic mechanism — full versus staged task disclosure

**Concern.** Persistence might be advance planning: a model shown all ten tasks
upfront could pick one ecosystem for the whole set at the start.

**Why.** Generate one file per request, A1 first, revealing either the full task
list or only the current task, each in a fresh conversation. Logs and file
snapshots verify the generation order.

**Result.** Persistence conditional on an affiliated A1 survives when future
tasks are withheld: 89.4% full versus 75.5% staged (Gemini 2.5 Flash), 87.0%
versus 87.2% (GPT-5.4 Mini), 65.4% versus 66.2% (Nova Pro).

## 5–10. Pipeline analyses

Each has its own README; in short:

- **`agent_runtime`** — VIB keeps its sign on both OpenCode and the OpenAI
  Agents SDK for 6 of 7 affiliated models. Magnitudes are generally smaller
  under the SDK, so the sign is robust and the effect size is runtime-sensitive.
- **`control_composition`** — every significantly positive effect stays positive
  in all seven control subsets (6/6 direct, 7/7 agentic); switching aggregation
  rule moves VIB by at most 0.015.
- **`affiliation_definition`** — under the merged definition GPT-5.4's direct
  VIB is not distinguishable from zero; restricted to OpenAI surfaces it is
  significantly positive. Merging dilutes the signal rather than creating it.
- **`concentration_vs_affiliation`** — VIB correlates −0.015 (direct) and
  +0.125 (agentic) with the normalized Gini Index, so it is not a restatement
  of concentration.
- **`prompt_format`** — mean VIB is positive under every prompt format, though
  individual models vary.
- **`option_order`** — reordering does not remove affiliated selection and the
  pooled First−Last contrast is not significant (−3.3 pp, 95% CI [−7.4, +0.8]).
  Omitting the option drops every model below 2%.

---

## Layout

```
code/ablations/
  initial_provider/     assigned_as_code/   by_instruction/
  agentic_mechanism/    single_shot_multifile/   task_disclosure/
  shared/               campaign launcher, runner, sampling audit, protocol tests
  paper_inputs/         the paper's archived prompts, per scenario
  anchor_files/         supplied A1 implementations (anchor_aws/, anchor_google/)
  snapshots/            recorded analysis snapshots + the two result generators
  diffs/                prompt diffs against the paper's config
```

Campaign runs live beside the rest of the data, grouped the same way:

```
outputs/ablations/
  initial_provider/assigned_as_code/     a1_completion_20s_3m_5c, _300s
    microsoft_openai/                    a1_microsoft_openai_20s_3m_5c
  initial_provider/by_instruction/       a3_instructed_anchor_20s_extension_5c, _8s_3m_5c
    microsoft_openai/                    a3_microsoft_openai_20s_3m_5c
  agentic_mechanism/single_shot_multifile/   a2_single_shot_20s_extension_5c, _8s_3m_5c
  agentic_mechanism/task_disclosure/     a4_disclosure_20s_extension_3m_5c, _6s_3m_5c, _300s

```

Each run directory holds `plan.json` (with the `code_sha256` map),
`progress.json`, `runtime.json`, `logs/`, and `runs/` — the agentic session
workspaces, which are the generated repositories themselves.

Ablation 1 ran in two passes. A suite-wide execution launched by
`shared/scripts/run_sequential.sh` was interrupted partway — five models aborted
after three consecutive failures — and `a1_completion_20s_3m_5c` then resumed
from it, retaining 254 already-finished attempts rather than re-paying for them.

Those 254 attempts are **materialised in `a1_completion_20s_3m_5c/runs/`**, each
verified against the `artifacts_sha256` its `plan.json` records, so this one
directory is the complete ablation-1 output and the interrupted predecessor is
not shipped. `plan.json` keeps the full `retained_attempts` list, including each
attempt's original `source_attempt` path, with
`retained_attempts_materialized: true`.

One consequence to be aware of: that run's `plan.json` describes the completion
pass only (346 cells), while `runs/` holds attempts for 375 cells — the extra
254 belong to the predecessor's plan. `progress.json` likewise reports
`attempted: 121`, which describes the execution rather than the directory's
contents.

Only runs that a snapshot or a successor's manifest cites are kept;
single-model pilots, smoke runs and pre-flight credential checks were dropped.
`scripts/continue.py` is the resume tool that produced this run and is recorded
in its `code_sha256`; it now requires `--previous` explicitly, since the shipped
run needs no predecessor.

### Naming and provenance

Campaign directories are named for what they test, but the `--ablation` ids stay
numeric (`1`–`4`, and `1/microsoft_openai` for the nested Microsoft-OpenAI
extension) because they appear in archived run manifests and inside the analysis
snapshots. `shared/common.py` maps an id to its directory via `ablation_dir()`,
and `shared/scripts/run_sequential.sh` maps a stage number the same way:

| Ablation id | Directory |
| --- | --- |
| 1 | `initial_provider/assigned_as_code` |
| 2 | `agentic_mechanism/single_shot_multifile` |
| 3 | `initial_provider/by_instruction` |
| 4 | `agentic_mechanism/task_disclosure` |

The snapshots under `snapshots/` are kept byte-for-byte as recorded, including
their original `ablation_2` / `ablation_3` keys and their `script_sha256`
fields; `snapshots/make_summaries.py` translates between those keys and the
directory names.

Provider credentials are redacted out of the archived runtime configs by
`shared/common.py` before they are written: the `apiKey` fields in each
attempt's `opencode.json` read `[REDACTED]`, and redaction markers appear in
3,646 files. A scan of all 155,614 files found no credential-shaped strings and
no values from `configs/.env` other than public API endpoints.

### Rebuilding

All ten ablations' derived tables live in `outputs/tables/`, beside the data
rather than beside the code. Rebuild them from `code/`:

```bash
python ablations/snapshots/make_summaries.py        # the four campaigns
python ablations/snapshots/make_paper_summaries.py  # control_composition,
                                                    # prompt_format,
                                                    # concentration_vs_affiliation,
                                                    # affiliation_definition,
                                                    # agent_runtime
```

Each campaign is launched from its own `scripts/run.py` and is resumable.
Protocol and input-construction tests need no API keys:

```bash
python -m unittest ablations.shared.tests.test_inputs
python -m unittest ablations.agentic_mechanism.task_disclosure.tests.test_staged
```

Two attempt scopes are reported for the anchor and disclosure campaigns, since
agentic runs can hit the time budget and be retried. The scope reported in the
paper is marked in each `outputs/tables/<ablation>/summary.md`: `latest_finished` for the two
initial-provider campaigns, `first_attempt` for task disclosure.
