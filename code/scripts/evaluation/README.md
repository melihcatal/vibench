# Evaluation Scripts

- [`detect_services.py`](detect_services.py): provider and ecosystem detection.
- [`evaluate.py`](evaluate.py): direct benchmark metrics.
- [`evaluate_agentic.py`](evaluate_agentic.py): agentic benchmark metrics.
- [`generate_vibench_results_markdown.py`](generate_vibench_results_markdown.py): consolidated report helpers used by the current plotting scripts and result summaries.
- [`evaluate_gini.py`](evaluate_gini.py): paper-style provider Gini indices for no-input-code (`nli`) generations, using the scenario-wide provider union from [Zhang et al.](https://arxiv.org/abs/2501.07849).

Run the Gini analysis on the canonical direct results:

```bash
python scripts/evaluation/evaluate_gini.py --run direct/complete/full_5c
```

Outputs are written under the run's `analysis/gini_nli_provider/` directory.

Run all comparable prompt settings (direct NLI/FIM/Reference-Open and agentic
free/informed) with:

```bash
python scripts/evaluation/evaluate_gini_matrix.py
```

Run IDs can be flat legacy names or nested active paths such as
`direct/complete/full_5c` and `agentic/complete/opencode_full_5c`.

Multi-provider scoring defaults to share-normalized weighting in the direct and
agentic evaluators. Flattened suggestion share is kept as a comparison view.
