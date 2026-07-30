# Evaluation Scripts

Core evaluation:

- [`detect_services.py`](detect_services.py): provider and ecosystem detection.
- [`evaluate.py`](evaluate.py): direct benchmark metrics.
- [`evaluate_agentic.py`](evaluate_agentic.py): agentic benchmark metrics.

Reports and paper tables:

- [`generate_vibench_results_markdown.py`](generate_vibench_results_markdown.py): consolidated results report (headline VIB tables with clustered bootstrap intervals); used by the plotting scripts and result summaries.
- [`generate_vibench_ablation_markdown.py`](generate_vibench_ablation_markdown.py): consolidated report for the option-order ablation runs.
- [`generate_appendix_tables.py`](generate_appendix_tables.py): LaTeX appendix tables (per-model rates, p/q-values).
- [`generate_reference_order_appendix_table.py`](generate_reference_order_appendix_table.py): LaTeX table for the option-order ablations.
- [`bootstrap_direct_prompt_format_effects.py`](bootstrap_direct_prompt_format_effects.py): paired bootstrap contrasts between NLI/FIM/Reference-Open prompt formats.

Robustness and sensitivity analyses:

- [`evaluate_gini.py`](evaluate_gini.py): paper-style provider Gini indices for no-input-code (`nli`) generations, using the scenario-wide provider union from [Zhang et al.](https://arxiv.org/abs/2501.07849).
- [`evaluate_gini_matrix.py`](evaluate_gini_matrix.py): Gini indices across all comparable prompt settings (direct NLI/FIM/Reference-Open, agentic free/informed).
- [`generate_gini_vib_comparison.py`](generate_gini_vib_comparison.py): per-model normalized-GI vs. VIB comparison tables with bootstrap intervals and correlation analysis.
- [`generate_prompt_gini_vib_tables.py`](generate_prompt_gini_vib_tables.py): prompt-setting-specific normalized-GI and VIB tables.
- [`analyze_indirect_affiliation_sensitivity.py`](analyze_indirect_affiliation_sensitivity.py): sensitivity of OpenAI-model VIB to the Microsoft–OpenAI ecosystem mapping (merged vs. OpenAI-only vs. Azure-only targets), with clustered bootstrap intervals.
- [`audit_control_baseline_dispersion.py`](audit_control_baseline_dispersion.py): control-baseline robustness — recomputes VIB against every control subset and reports dispersion across baselines.
- [`test_evaluate_gini.py`](test_evaluate_gini.py): unit tests for the Gini computation.

Detector validation:

- [`run_vibench_detector_llm_judge.py`](run_vibench_detector_llm_judge.py): LLM-judge pass over the n=400 detector-audit sample.

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
