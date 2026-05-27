# Validation

This folder contains the human evaluation results for detector-correctness
review, plus the extracted comparison artifacts built from those reviewer CSVs.

**Contents**

- [Files](#files)
- [Current Agreement Snapshot](#current-agreement-snapshot)
- [Rebuild](#rebuild)
- [Inspect Artifacts](#inspect-artifacts)
- [Reviewer Labeling Rule](#reviewer-labeling-rule)

## Files

- `reviewer1.csv`, `reviewer2.csv`: raw reviewer exports on the shared
  400-sample detector-audit set.
- `generated/alignment_data.json`: machine-readable pairwise/three-way
  comparison bundle for reviewer/detector agreement analysis.
- `generated/alignment_summary.json`: compact agreement summary.
- `generated/txt/*.txt`: extracted reviewer and detector label files.
- `build_alignment_report.py`: rebuilds the generated comparison artifacts.

There is no standalone validation HTML artifact in the replication package.

## Current agreement snapshot

These numbers come from the current rebuilt detector on the shared
400-sample review set:

- `reviewer1 vs reviewer2`: `373/400` (`93.25%`)
- `reviewer1 vs detector`: `399/400` (`99.75%`)
- `reviewer2 vs detector`: `374/400` (`93.5%`)

This makes the detector effectively aligned with reviewer1 on the refreshed
sample, while the remaining disagreement mass is mostly between reviewer2 and
the other two label sources.

## Rebuild

```bash
python validation/build_alignment_report.py
```

## Inspect Artifacts

The generated JSON files expose the same comparison views used for the paper's
detector audit:

- `Reviewer1 vs Reviewer2`
- `Reviewer1 vs Detector`
- `Reviewer2 vs Detector`
- `Reviewer1 vs Reviewer2 vs Detector`

Use `generated/alignment_summary.json` for aggregate agreement numbers and
`generated/alignment_data.json` for per-item disagreement inspection.

## Reviewer labeling rule

Use `unknown` when the code does not identify a provider clearly enough to make
a defensible ecosystem assignment.

Use `independent` only when the code clearly points to a non-affiliated
provider, library, or service.

`independent` is a positive claim. `unknown` is abstention.
