# Prompt-format robustness — headline

Derived from `table_b_vib.csv` by `ablations/snapshots/make_paper_summaries.py`.

| Prompt format | Affiliated models | Mean VIB | Models with positive VIB |
| --- | --- | --- | --- |
| `direct_nli` | 10 | +0.021 | 5/10 |
| `direct_fim` | 10 | +0.039 | 6/10 |
| `direct_reference_open` | 10 | +0.029 | 5/10 |
| `agentic_free` | 7 | +0.189 | 6/7 |
| `agentic_informed` | 7 | +0.145 | 7/7 |

Mean VIB is positive under every prompt format, in both the direct and agentic settings. Individual models vary: the aggregate effect does not depend on one wording, but it is not present in every model under every format.
