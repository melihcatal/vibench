# Evaluation Scripts

Grouped into folders by role. The modules form one flat namespace — each file
adds the sibling groups to `sys.path` — so the grouping is for navigation and
does not change how they import each other.

```
core/         model_registry, detect_services, evaluate, evaluate_agentic,
              generate_vibench_results_markdown, heuristics/
gini/         concentration measures and the Gini-vs-VIB comparison
tables/       control-baseline dispersion, affiliation sensitivity,
              prompt-format bootstrap, appendix-table builders
baselines/    packaging a run's control outputs for --baseline
audit/        detector LLM-judge run
```

`core/heuristics/` holds the provider-attribution rules as JSON; see its README.

Core evaluation:

- [`core/model_registry.py`](core/model_registry.py): single source of truth for study-model metadata — control baseline, study membership, canonical table order, ecosystems, tiers, and default display names — backed by `benchmark/vibench/models.json` (`study_order` + `role` fields). Scripts must derive model lists from here instead of hard-coding them; per-artifact label dicts may override display names but fall back to the registry.
- [`core/detect_services.py`](core/detect_services.py): provider and ecosystem detection.
- [`core/evaluate.py`](core/evaluate.py): direct benchmark metrics.
- [`core/evaluate_agentic.py`](core/evaluate_agentic.py): agentic benchmark metrics.

Reports and paper tables:

- [`core/generate_vibench_results_markdown.py`](core/generate_vibench_results_markdown.py): consolidated results report (headline VIB tables with clustered bootstrap intervals); used by the plotting scripts and result summaries.
- [`tables/generate_vibench_ablation_markdown.py`](tables/generate_vibench_ablation_markdown.py): consolidated report for the option-order ablation runs.
- [`tables/generate_appendix_tables.py`](tables/generate_appendix_tables.py): LaTeX appendix tables (per-model rates, p/q-values).
- [`tables/generate_reference_order_appendix_table.py`](tables/generate_reference_order_appendix_table.py): LaTeX table for the option-order ablations.
- [`tables/bootstrap_direct_prompt_format_effects.py`](tables/bootstrap_direct_prompt_format_effects.py): paired bootstrap contrasts between NLI/FIM/Reference-Open prompt formats.

Robustness and sensitivity analyses:

- [`gini/evaluate_gini.py`](gini/evaluate_gini.py): paper-style provider Gini indices for no-input-code (`nli`) generations, using the scenario-wide provider union from [Zhang et al.](https://arxiv.org/abs/2501.07849).
- [`gini/evaluate_gini_matrix.py`](gini/evaluate_gini_matrix.py): Gini indices across all comparable prompt settings (direct NLI/FIM/Reference-Open, agentic free/informed).
- [`gini/generate_gini_vib_comparison.py`](gini/generate_gini_vib_comparison.py): per-model normalized-GI vs. VIB comparison tables with bootstrap intervals and correlation analysis.
- [`gini/generate_prompt_gini_vib_tables.py`](gini/generate_prompt_gini_vib_tables.py): prompt-setting-specific normalized-GI and VIB tables.
- [`tables/analyze_indirect_affiliation_sensitivity.py`](tables/analyze_indirect_affiliation_sensitivity.py): sensitivity of OpenAI-model VIB to the Microsoft–OpenAI ecosystem mapping (merged vs. OpenAI-only vs. Azure-only targets), with clustered bootstrap intervals.
- [`tables/audit_control_baseline_dispersion.py`](tables/audit_control_baseline_dispersion.py): control-baseline robustness — recomputes VIB against every control subset and reports dispersion across baselines.
- [`gini/test_evaluate_gini.py`](gini/test_evaluate_gini.py): unit tests for the Gini computation.

Detector validation:

- [`audit/run_vibench_detector_llm_judge.py`](audit/run_vibench_detector_llm_judge.py): LLM-judge pass over the n=400 detector-audit sample.

Run the Gini analysis on the canonical direct results:

```bash
python scripts/evaluation/gini/evaluate_gini.py --run direct/complete/full_5c
```

Outputs are written under the run's `analysis/gini_nli_provider/` directory.

Run all comparable prompt settings (direct NLI/FIM/Reference-Open and agentic
free/informed) with:

```bash
python scripts/evaluation/gini/evaluate_gini_matrix.py
```

Run IDs can be flat legacy names or nested active paths such as
`direct/complete/full_5c` and `agentic/complete/opencode_full_5c`.

Multi-provider scoring defaults to share-normalized weighting in the direct and
agentic evaluators. Flattened suggestion share is kept as a comparison view.
