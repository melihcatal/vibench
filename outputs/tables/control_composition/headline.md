# Control-composition sensitivity — headline

Derived from `control_subset_sensitivity.csv` and the VIB point estimates in `../concentration_vs_affiliation/gini_vib_per_model.csv` by `ablations/snapshots/make_paper_summaries.py`.

| Setting | Affiliated models | Significantly positive VIB | Of those, positive in every subset |
| --- | --- | --- | --- |
| direct | 10 | 6 | 6/6 |
| agentic | 7 | 7 | 7/7 |

Subsets are the seven non-empty subsets of the three non-affiliated controls.

Alternative aggregation rules, as absolute change in VIB against the unweighted mean used in the paper:

- pooled instead of mean: max 0.0000, median 0.0000
- median instead of mean: max 0.0154, median 0.0085
