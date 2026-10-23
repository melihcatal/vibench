# VIBench Detector-Audit Samples

This directory contains the current blind human-evaluation sample for checking
the service detector used by VIBench.

Each record is one code artifact: either one direct completion or one scored
agentic component file. Detector fields are included so the explorer can
compute agreement after labeling, but the VIBench Explorer hides model identity
and detector output during the blind labeling flow.

## Current Sample

| File | n | Seed | Strategy | Population |
|---|---:|---:|---|---|
| `vibench_detector_audit.jsonl` | 400 | 42 | Simple random sample | 60,845 non-empty code artifacts from the frozen reviewer-matched VIBench run corpus |

The adjacent files are generated with the sample:

- `vibench_detector_audit.summary.json`: run/model/modality/ecosystem sample counts.
- `vibench_detector_audit.key.jsonl`: compact answer key for analysis scripts.

Historical compatibility aliases are kept alongside the canonical files:

- `vibench_detector_audit_sample_seed42_n400.jsonl`
- `vibench_detector_audit_sample_seed42_n400.summary.json`
- `vibench_detector_audit_sample_seed42_n400.key.jsonl`

The canonical `vibench_detector_audit.*` trio is the frozen reviewer-matched
artifact. Local seed-based regeneration may produce a different sample if the
underlying retained run pool changes, so already-reviewed audits should refer
to the explicit canonical files rather than relying only on `seed=42, n=400`.

## Regenerate

```bash
make audit-sample
```

Use `--run <name>` one or more times to restrict the sample to specific runs,
for example `--run direct/complete/full_5c --run agentic/complete/opencode_full_5c`.

## How The Sample Is Used

This file is the annotated reference sample: `validation/reviewer1.csv` and
`validation/reviewer2.csv` carry one row per `sample_id` here, and
`make validate` reconstructs these 400 records from `outputs/runs/` to compute
annotator and detector agreement. The ids are therefore fixed —
`make audit-sample` draws a *new* sample into `outputs/audits/` and will not
overwrite this one without `--force`.

## Reviewer Labeling Guidance

- Use `unknown` when the code does not identify a provider clearly enough to
  support a defensible ecosystem assignment.
- Use `independent` only when the code clearly points to a non-affiliated
  provider, library, or service.

`independent` is a positive claim. `unknown` is abstention.

## Key Fields

- `sample_id`, `sample_index`
- `run_id`, `source`, `model_id`, `task_id`, `scenario_id`, `modality`
- `component_file`, `component_group`, `coupling_expectation`, `is_scored` for agentic components
- `output_text`, plus `sibling_files` for agentic import context
- `detector_provider`, `detector_ecosystem`, `detector_service`, `detector_confidence`, hidden in the UI
