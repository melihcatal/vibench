#!/usr/bin/env python3
"""Generate a LaTeX appendix table for Reference-Open option-order ablations."""

from __future__ import annotations

from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import sys as _sys
from pathlib import Path as _Path
# The evaluation modules form one namespace, grouped into folders for
# readability only, so every group is importable from every other.
_EVAL_DIR = _Path(__file__).resolve().parents[1]
for _group in ("core", "gini", "tables", "baselines", "audit"):
    _sys.path.insert(0, str(_EVAL_DIR / _group))
import evaluate as direct_eval  # noqa: E402
import generate_vibench_ablation_markdown as ablation  # noqa: E402
import generate_appendix_tables as appendix_tables  # noqa: E402


# Resolve against the repository, not the current directory: a bare relative path
# created a stray code/paper/ tree wherever the script happened to be run from.
OUTPUT_PATH = (Path(__file__).resolve().parents[4]
               / "outputs" / "tables" / "option_order" / "reference_order_ablation.tex")
CONDITIONS = ["Balanced", "First", "Middle", "Last", "Omitted"]


def pct(value: float | None) -> str:
    if value is None:
        return "--"
    return f"{100.0 * value:.1f}"


def pp(value: float | None) -> str:
    if value is None:
        return "--"
    if abs(value) < 0.0005:
        value = 0.0
    return f"{100.0 * value:+.1f}"


def ci_pp(value: tuple[float, float] | None) -> str:
    if value is None:
        return "--"
    return f"[{pp(value[0])}, {pp(value[1])}]"


def q_value(value: float | None) -> str:
    if value is None:
        return "--"
    return f"{value:.4f}"


def p_value(value: float | None) -> str:
    return q_value(value)


def q_marker(value: float | None) -> str:
    if value is None:
        return ""
    if value < 0.05:
        return r"$^{*}$"
    return ""


def render_table() -> str:
    models_info = direct_eval.load_models("vibench")
    model_ids = ablation.discover_ablation_models(models_info)
    summaries, _run_dirs = ablation.build_direct_summaries(models_info, model_ids)

    pooled_rows = ablation.pooled_contrast_rows(
        summaries,
        [
            ("First", "Last"),
            ("First", "Balanced"),
            ("Omitted", "Balanced"),
        ],
        "direct_ablation",
    )
    pooled_contrast = next(row for row in pooled_rows if row["contrast"] == "First - Last")
    model_contrasts = {
        row["model_id"]: row
        for row in ablation.model_contrast_rows(
            "First",
            summaries["First"],
            "Last",
            summaries["Last"],
            "direct_first_last",
            model_ids,
        )
    }

    lines = [
        r"\subsection{Reference-Open Option-Order Ablation}",
        r"\begin{table}[p]",
        r"\centering",
        r"\scriptsize",
        r"\setlength{\tabcolsep}{2.5pt}",
        r"\renewcommand{\arraystretch}{1.12}",
        r"\caption{Impact of provider-option order in the direct Reference-Open setting. The table reports affiliated-ecosystem selection rates for the four focused affiliated models. \textit{Balanced} is the retained benchmark setting with randomized option order; \textit{First}, \textit{Middle}, and \textit{Last} place the affiliated option in the corresponding position; \textit{Omitted} removes the affiliated option from the prompt. $\Delta$ reports First minus Last in percentage points with bootstrap confidence intervals, bootstrap $p$-values, and FDR-adjusted $q$-values. Asterisks mark FDR-adjusted significance within the per-model First--Last contrasts ($^{*}q<0.05$).}",
        r"\label{tab:appendix-reference-order-ablation}",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{>{\raggedright\arraybackslash}p{2.65cm} *{5}{>{\centering\arraybackslash}p{1.05cm}} >{\centering\arraybackslash}p{1.10cm} >{\centering\arraybackslash}p{2.10cm} >{\centering\arraybackslash}p{0.85cm} >{\centering\arraybackslash}p{0.85cm}}",
        r"\toprule",
        r"\multirow{2}{*}{Model} & \multicolumn{5}{c}{Affiliated selection rate} & \multicolumn{4}{c}{Order contrast} \\",
        r"\cmidrule(lr){2-6}\cmidrule(lr){7-10}",
        r"& Balanced & First & Middle & Last & Omitted & $\Delta$ & 95\% CI & $p$ & $q$ \\",
        r"\midrule",
    ]

    pooled_cells = [
        r"\textit{Pooled}",
        pct(summaries["Balanced"].get("rate")),
        pct(summaries["First"].get("rate")),
        pct(summaries["Middle"].get("rate")),
        pct(summaries["Last"].get("rate")),
        pct(summaries["Omitted"].get("rate")),
        pp(pooled_contrast.get("delta")) + q_marker(pooled_contrast.get("q_value")),
        ci_pp(pooled_contrast.get("ci")),
        p_value(pooled_contrast.get("p_value")),
        q_value(pooled_contrast.get("q_value")),
    ]
    lines.append(" & ".join(pooled_cells) + r" \\")
    lines.append(r"\midrule")

    for model_id in model_ids:
        contrast = model_contrasts[model_id]
        cells = [
            appendix_tables.escape_latex(appendix_tables.MODEL_LABELS[model_id]),
            *[pct(summaries[condition]["by_model"][model_id].get("rate")) for condition in CONDITIONS],
            pp(contrast.get("delta")) + q_marker(contrast.get("q_value")),
            ci_pp(contrast.get("ci")),
            p_value(contrast.get("p_value")),
            q_value(contrast.get("q_value")),
        ]
        lines.append(" & ".join(cells) + r" \\")

    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"}",
        r"\end{table}",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_table())
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
