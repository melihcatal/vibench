# Evaluation Scripts

- [`detect_services.py`](detect_services.py): provider and ecosystem detection.
- [`evaluate.py`](evaluate.py): direct benchmark metrics.
- [`evaluate_agentic.py`](evaluate_agentic.py): agentic benchmark metrics.
- [`generate_vibench_results_markdown.py`](generate_vibench_results_markdown.py): consolidated report helpers used by the current plotting scripts and result summaries.

Run IDs can be flat legacy names or nested active paths such as
`direct/complete/full_5c` and `agentic/complete/opencode_full_5c`.

Multi-provider scoring defaults to share-normalized weighting in the direct and
agentic evaluators. Flattened suggestion share is kept as a comparison view.
