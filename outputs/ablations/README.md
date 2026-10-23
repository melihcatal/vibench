# Ablation campaign runs

Output of the four ablation campaigns, each launched by its own runner under
`code/ablations/<group>/<campaign>/scripts/run.py`. Grouped to mirror the code.

A campaign run directory holds:

| | |
|---|---|
| `plan.json` | every planned cell, the sampling policy, and a `code_sha256` map over the main runners, `models.json` and both paper configs — so the run is tied to the exact code and design it ran against |
| `progress.json` | what was attempted, completed, failed, and whether the run was interrupted |
| `runtime.json` | Python version, package versions, OpenCode version |
| `logs/` | per-model attempt log, one JSONL per model |
| `runs/` | the generated repositories, as `<scenario>/<model>/<condition>/r<NNN>/attempt_<NNN>/` |

## Why each campaign has more than one run

These are long, paid runs. When one hit a time budget or a model aborted after
repeated failures, the next run **resumed** rather than re-paying: it retains
the attempts that already finished, recorded in its `plan.json` as
`retained_attempts` with each attempt's `source_attempt` path and
`artifacts_sha256`, plus `previous_plan_sha256` so the reuse can be re-verified.

So within a campaign the runs form a chain, and the later ones are smaller
because they only ran what was left. Reading any one alone understates the
campaign. The per-campaign README in each directory says which run is which.

One exception: ablation 1's first pass came from a suite-wide execution that was
interrupted after stage 1. Its 254 reused attempts were verified against their
recorded hashes and materialised into `a1_completion_20s_3m_5c/runs/`, so that
predecessor is not shipped separately — see that campaign's README.

## Where the numbers come from

None of the result tables are computed from these directories directly. They
come from the analysis snapshots in `code/ablations/snapshots/`, which were
recorded when the campaigns finished and carry their own `script_sha256`. The
tables are rebuilt from those snapshots with
`python ablations/snapshots/make_summaries.py` (run from `code/`).

These run directories are the underlying record: the prompts sent, the code
generated, and what succeeded or failed.
