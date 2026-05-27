#!/usr/bin/env python3
"""Bootstrap direct prompt-format VIB effects over affiliated models."""

from __future__ import annotations

import argparse
import json
import random
import statistics
from pathlib import Path

import generate_appendix_tables as appendix_tables


PROMPTS = [
    ("nli", "NLI"),
    ("fim", "FIM"),
    ("reference_open", "Ref.-Open"),
]

CONTRASTS = [
    ("fim", "nli", "FIM - NLI"),
    ("reference_open", "nli", "Ref.-Open - NLI"),
    ("reference_open", "fim", "Ref.-Open - FIM"),
]


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def sample_sd(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return statistics.stdev(values)


def percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("Cannot compute a percentile over an empty sample.")
    pos = q * (len(ordered) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(ordered) - 1)
    frac = pos - lo
    return ordered[lo] * (1.0 - frac) + ordered[hi] * frac


def ci(values: list[float]) -> list[float]:
    return [percentile(values, 0.025), percentile(values, 0.975)]


def empirical_p_value(samples: list[float]) -> float:
    """Two-sided bootstrap p-value for a zero-centered null."""
    n = len(samples)
    le_zero = sum(1 for value in samples if value <= 0.0)
    ge_zero = sum(1 for value in samples if value >= 0.0)
    lower_tail = (le_zero + 1) / (n + 1)
    upper_tail = (ge_zero + 1) / (n + 1)
    return min(1.0, 2.0 * min(lower_tail, upper_tail))


def benjamini_hochberg(p_values: list[float]) -> list[float]:
    m = len(p_values)
    order = sorted(range(m), key=lambda idx: p_values[idx])
    q_values = [1.0] * m
    running_min = 1.0
    for rank, idx in reversed(list(enumerate(order, start=1))):
        running_min = min(running_min, p_values[idx] * m / rank)
        q_values[idx] = min(running_min, 1.0)
    return q_values


def parse_prompt_values(input_path: Path) -> list[dict[str, float | str]]:
    root_map = appendix_tables.get_root_map(input_path)
    direct_vib = {
        row["Model"]: row
        for row in appendix_tables.root_table(root_map, "Direct VIB Significance")
    }
    prompt_values = appendix_tables.compute_direct_prompt_vib_rows(direct_vib)

    rows: list[dict[str, float | str]] = []
    for model_id in appendix_tables.ADJUSTED_MODEL_ORDER:
        values = prompt_values.get(model_id, {})
        parsed = {
            key: appendix_tables.to_float(values.get(key, "--"))
            for key, _label in PROMPTS
        }
        if any(value is None for value in parsed.values()):
            continue
        rows.append({
            "model_id": model_id,
            "model": appendix_tables.MODEL_LABELS[model_id],
            **parsed,
        })

    if len(rows) < 2:
        raise ValueError("Need at least two affiliated models for model-level bootstrap.")
    return rows


def prompt_vector(rows: list[dict[str, float | str]], key: str) -> list[float]:
    return [float(row[key]) for row in rows]


def bootstrap(rows: list[dict[str, float | str]], n_bootstrap: int, seed: int) -> dict:
    rng = random.Random(seed)
    n_models = len(rows)

    summary_samples = {
        key: {"mean": [], "sd": []}
        for key, _label in PROMPTS
    }
    contrast_samples = {
        label: {"mean_delta": [], "sd_delta": []}
        for _left, _right, label in CONTRASTS
    }

    for _ in range(n_bootstrap):
        sample = [rows[rng.randrange(n_models)] for _ in range(n_models)]
        for key, _label in PROMPTS:
            values = prompt_vector(sample, key)
            summary_samples[key]["mean"].append(mean(values))
            summary_samples[key]["sd"].append(sample_sd(values))
        for left, right, label in CONTRASTS:
            left_values = prompt_vector(sample, left)
            right_values = prompt_vector(sample, right)
            paired_diffs = [lval - rval for lval, rval in zip(left_values, right_values)]
            contrast_samples[label]["mean_delta"].append(mean(paired_diffs))
            contrast_samples[label]["sd_delta"].append(sample_sd(left_values) - sample_sd(right_values))

    prompt_summary = []
    for key, label in PROMPTS:
        values = prompt_vector(rows, key)
        prompt_summary.append({
            "prompt": key,
            "label": label,
            "mean": mean(values),
            "mean_ci": ci(summary_samples[key]["mean"]),
            "sd": sample_sd(values),
            "sd_ci": ci(summary_samples[key]["sd"]),
        })

    contrast_rows = []
    mean_p_values = []
    sd_p_values = []
    for left, right, label in CONTRASTS:
        left_values = prompt_vector(rows, left)
        right_values = prompt_vector(rows, right)
        paired_diffs = [lval - rval for lval, rval in zip(left_values, right_values)]
        mean_samples = contrast_samples[label]["mean_delta"]
        sd_samples = contrast_samples[label]["sd_delta"]
        mean_p = empirical_p_value(mean_samples)
        sd_p = empirical_p_value(sd_samples)
        mean_p_values.append(mean_p)
        sd_p_values.append(sd_p)
        contrast_rows.append({
            "contrast": label,
            "mean_delta": mean(paired_diffs),
            "mean_ci": ci(mean_samples),
            "mean_p": mean_p,
            "sd_delta": sample_sd(left_values) - sample_sd(right_values),
            "sd_ci": ci(sd_samples),
            "sd_p": sd_p,
        })

    mean_q_values = benjamini_hochberg(mean_p_values)
    sd_q_values = benjamini_hochberg(sd_p_values)
    for row, mean_q, sd_q in zip(contrast_rows, mean_q_values, sd_q_values):
        row["mean_q"] = mean_q
        row["sd_q"] = sd_q

    return {
        "unit": "provider-affiliated direct-evaluation model",
        "n_models": n_models,
        "n_bootstrap": n_bootstrap,
        "seed": seed,
        "models": [row["model_id"] for row in rows],
        "prompt_summary": prompt_summary,
        "contrasts": contrast_rows,
    }


def fmt_pp(value: float) -> str:
    if abs(value) < 0.05:
        value = 0.0
    return f"{value:+.1f}"


def fmt_unsigned(value: float) -> str:
    if abs(value) < 0.05:
        value = 0.0
    return f"{value:.1f}"


def fmt_ci(values: list[float]) -> str:
    return f"[{fmt_pp(values[0])}, {fmt_pp(values[1])}]"


def fmt_unsigned_ci(values: list[float]) -> str:
    return f"[{fmt_unsigned(values[0])}, {fmt_unsigned(values[1])}]"


def fmt_q(value: float) -> str:
    if value < 0.001:
        return r"$<0.001$"
    return f"{value:.3f}"


def render_latex_table(results: dict) -> str:
    lines = [
        r"\subsection{Direct Prompt-Format Bootstrap Sensitivity}",
        r"\begin{table}[p]",
        r"\centering",
        r"\scriptsize",
        r"\setlength{\tabcolsep}{3pt}",
        r"\renewcommand{\arraystretch}{1.12}",
        r"\caption{Model-level paired bootstrap sensitivity analysis for direct prompt-format effects. Panel A reports the mean direct \ac{vib} and cross-model standard deviation across the ten provider-affiliated direct models. Panel B reports paired prompt-format contrasts. Values are percentage points; $q$ values are Benjamini--Hochberg adjusted within the three mean contrasts and within the three standard-deviation contrasts.}",
        r"\label{tab:appendix-direct-prompt-bootstrap}",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{>{\raggedright\arraybackslash}p{2.80cm} >{\centering\arraybackslash}p{1.10cm} >{\centering\arraybackslash}p{2.10cm} >{\centering\arraybackslash}p{1.10cm} >{\centering\arraybackslash}p{2.10cm} >{\centering\arraybackslash}p{0.95cm} >{\centering\arraybackslash}p{0.95cm}}",
        r"\toprule",
        r"\multicolumn{7}{l}{\textit{Panel A: Prompt-format summaries}} \\",
        r"Prompt format & Mean VIB & 95\% CI & SD & 95\% CI & & \\",
        r"\midrule",
    ]
    for row in results["prompt_summary"]:
        lines.append(
            " & ".join([
                row["label"],
                fmt_pp(row["mean"]),
                fmt_ci(row["mean_ci"]),
                fmt_unsigned(row["sd"]),
                fmt_unsigned_ci(row["sd_ci"]),
                "",
                "",
            ])
            + r" \\"
        )

    lines += [
        r"\midrule",
        r"\multicolumn{7}{l}{\textit{Panel B: Pairwise contrasts}} \\",
        r"Contrast & $\Delta$ Mean & 95\% CI & $\Delta$ SD & 95\% CI & $q_{\Delta\mu}$ & $q_{\Delta\sigma}$ \\",
        r"\midrule",
    ]
    for row in results["contrasts"]:
        lines.append(
            " & ".join([
                row["contrast"],
                fmt_pp(row["mean_delta"]),
                fmt_ci(row["mean_ci"]),
                fmt_pp(row["sd_delta"]),
                fmt_ci(row["sd_ci"]),
                fmt_q(row["mean_q"]),
                fmt_q(row["sd_q"]),
            ])
            + r" \\"
        )

    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"}",
        r"\end{table}",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap direct prompt-format VIB effects over affiliated models.")
    parser.add_argument("--input", required=True, help="Path to current_results.md.")
    parser.add_argument("--json-out", required=True, help="Path for machine-readable bootstrap results.")
    parser.add_argument("--tex-out", required=True, help="Path for appendix LaTeX table.")
    parser.add_argument("--n-bootstrap", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=20260517)
    args = parser.parse_args()

    rows = parse_prompt_values(Path(args.input))
    results = bootstrap(rows, args.n_bootstrap, args.seed)
    json_out = Path(args.json_out)
    tex_out = Path(args.tex_out)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    tex_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(results, indent=2) + "\n")
    tex_out.write_text(render_latex_table(results))


if __name__ == "__main__":
    main()
