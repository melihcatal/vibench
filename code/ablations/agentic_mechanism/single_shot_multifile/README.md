# Ablation 2: single-shot multi-file generation

Tests whether provider selection and downstream persistence remain observable
when the same ten-file task is generated in one response, without agent tools.
Compare descriptively with the archived agentic NLI runs on the same scenarios;
the historical agentic baseline is not rerun by default. Unlike ablation 1,
the model generates A1 itself rather than receiving supplied code.

## Active scope

`config.yaml` selects Gemini 2.5 Flash, Nova Pro, and GPT-5.4 Mini, with five
planned repetitions per scenario: **120 single-shot runs**. Models run in parallel.

| Scenario | Task area |
|---|---|
| S03 | General text translation |
| S04 | Batch speech-to-text |
| S07 | OCR |
| S10 | Hosted LLM inference |
| S14 | Managed object storage |
| S16 | Secret management |
| S18 | Pub/Sub messaging |
| S20 | Managed log ingestion/query |

These retain ablation 4's six scenarios and add OCR and messaging for task
coverage, not selection by observed ablation scores. Ablation 4 remains unchanged.

The timeout is **300 seconds per complete ten-file response**, not per file.
Worker shutdown may add a few seconds. Sampling inherits the original paper
YAMLs, including GPT reasoning `none`; this ablation's shorter timeout is an
explicit budget difference from the historical agentic runs.

## Run

From `code/`, with the project's environment activated:

```bash
python -u -B ablations/agentic_mechanism/single_shot_multifile/scripts/run.py \
  --config ablations/agentic_mechanism/single_shot_multifile/config.yaml \
  --output ablations/outputs/a2_single_shot_8s_3m_5c \
  --execute
```

Omit `--execute` and add `--check` for offline validation. Credentials are loaded
from `code/configs/.env`. Nova returned HTTP 429 with an Amazon authentication
error on 2026-09-19; verify restored access before starting its paid runs.

## Protocol and interpretation

The wrapper calls the original direct generator and strictly parses a JSON
mapping of filenames to source. Only file-delivery instructions change in the
archived user and agent/system prompts; task specifications remain unchanged.
All 20 scenarios remain available through CLI/YAML selection. Prompt diffs are
in `../../diffs/agentic_mechanism/single_shot_multifile/`.

Report initial selections, affiliated shares, conditional downstream persistence,
eligibility, completion, and missing/unknown rates. Preserve failed attempts and
raw responses; do not replace failures until five successful runs are obtained.
No new controls are scheduled, so these are not fresh control-relative VIB scores.
Historical comparisons cannot isolate agency from route, date, output-format,
and runtime differences. See [RUNNING.md](../../shared/docs/RUNNING.md).

## Filename-only postprocessing

The strict runner rejects role labels included in JSON filename keys. A separate
postprocessor removes only `[SAME-SCENARIO] `, `[HELPER] `, `[LATER-STEP] `, or
their slash-separated equivalents when they map uniquely to the complete expected
filename set. It applies the same rule to every model; malformed JSON remains
unresolved. Source strings, including invalid Python or imports, are unchanged.

```bash
python -B ablations/agentic_mechanism/single_shot_multifile/scripts/normalize_filenames.py \
  --campaign ablations/outputs/a2_single_shot_8s_3m_5c
```

Derived repositories, recalculated metrics, per-response hashes and mappings, and
a summary are saved under the campaign's `filename_normalized/` directory.
Original responses, metrics, and failure statuses remain intact. Report this
postprocessing separately from strict-format success; it does not establish
code correctness. An existing derived directory is never overwritten.

## Extend to all 20 scenarios

Keep the completed eight-scenario campaign immutable. The extension launcher
uses `config_20_scenarios.yaml`, checks the old source/config hashes, input
fingerprints, sampling, timeout, and runtime versions, and retains all 120 old
attempts (including the 18 strict-format failures). It schedules only the 180
previously unattempted cells in a separate directory. No failed attempt is retried.

```bash
python -u -B ablations/agentic_mechanism/single_shot_multifile/scripts/extend.py \
  --config ablations/agentic_mechanism/single_shot_multifile/config_20_scenarios.yaml \
  --output ablations/outputs/a2_single_shot_20s_extension_5c \
  --check
```

Replace `--check` with `--execute` to run. Dry runs print previous attempts
skipped, any existing extension attempts skipped, and new scheduled runs.
Use `--resume` on subsequent invocations of this same extension plan. The saved
extension plan references the retained original attempts for combined analysis;
its local `runs/` directory contains only the additional twelve scenarios.
