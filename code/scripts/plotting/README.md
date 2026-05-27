# Plotting Scripts

- [`plot_vibench_claude_charts.py`](plot_vibench_claude_charts.py): high-resolution `claude_*.png` figures for the current direct, OpenCode agentic, transition, cascade, scenario, and ablation results.
- [`plot_vibench_overview_charts.py`](plot_vibench_overview_charts.py): compact SVG overview charts for direct, agentic, modality, and transition views.
- [`plot_vibench_multilabel_charts.py`](plot_vibench_multilabel_charts.py): compact SVG multi-label sensitivity and multi-provider prevalence charts.
- The rendered result charts used in the paper are bundled under [`docs/figures`](../../docs/figures). The scripts in this folder reproduce the equivalent charts directly from the bundled runs.

Preferred command:

```bash
make figures      # high-resolution claude_*.png charts
make figures-svg  # compact SVG overview / multi-label charts
```
