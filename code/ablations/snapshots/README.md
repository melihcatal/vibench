# Analysis snapshots

Recorded analysis results from when the campaigns finished. Each carries its own
`script_sha256` and hashes of the labels it read, so the result tables can be
rebuilt without re-running 1.5 GB of campaigns.

Kept byte-for-byte as recorded. They predate the current directory names, so
they still key campaigns as `ablation_2` / `ablation_3`;
`make_summaries.py` translates between those keys and the directory names.

## Read by the generators

| Snapshot | Feeds |
|---|---|
| `a1_a3_retry_snapshot_20260921_finished/bootstrap_results.json` | the anchor-retention tables for both initial-provider campaigns |
| `20260919_full_a2_a3/results.json` | the single-shot multi-file table |
| `20260920_a4_20s_finished_snapshot/results.json` | the full-versus-staged disclosure table |

Rebuild the tables with `python ablations/snapshots/make_summaries.py` from
`code/`. `make_paper_summaries.py` reads the derived tables that ship beside the
analyses rather than these snapshots.

## Kept as evidence, not read by the generators

| Snapshot | What it records |
|---|---|
| `20260920_a4_trace_audit/` | per-run trace audit over the fixed 580-run snapshot, first attempts only — the basis for the claim that generation order was verified |
| `a4_latest_trace_recheck_20260920T204543Z/` | a later re-check of the same audit, with an `anomalies` list |
| `20260920_final_ablations/` | closing audit across ablations 1 and 4, with the script that produced it |
| `20260920_combined_evidence/` | per-model selection contrasts and matched-comparator strata |
| `20260918_temporal_persistence/` | label and database manifests with run audit and statistics |

These are not inputs to any shipped table. They are the computed records behind
claims in the paper, so they are kept rather than regenerated — the campaigns
they summarise are paid runs.
