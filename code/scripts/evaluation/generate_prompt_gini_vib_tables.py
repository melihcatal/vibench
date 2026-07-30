#!/usr/bin/env python3
"""Generate prompt-specific normalized-GI and VIB tables with bootstrap CIs."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import evaluate as direct_eval  # noqa: E402
import evaluate_agentic as agentic_eval  # noqa: E402
import generate_vibench_results_markdown as reportlib  # noqa: E402
from evaluate_gini import compute_rows, flatten_agentic_results  # noqa: E402
from generate_gini_vib_comparison import (  # noqa: E402
    STRICT_CONTROLS,
    bootstrap_mean_ci,
    model_metadata,
)


SETTINGS = (
    ("direct_nli", "Direct NLI"),
    ("direct_fim", "Direct FIM"),
    ("direct_reference_open", "Direct REF"),
    ("agentic_free", "Agentic NLI"),
    ("agentic_informed", "Agentic REF"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build prompt-specific GI/VIB tables with 95% bootstrap CIs.")
    parser.add_argument("--direct-run", default="direct/complete/full_5c")
    parser.add_argument("--agentic-run", default="agentic/complete/opencode_full_5c")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/analysis/prompt_gini_vib_tables"))
    return parser.parse_args()


def gi_cells(direct_records: list[dict], agentic_results: list[dict]) -> dict[tuple[str, str], dict]:
    output = {}
    for setting, _ in SETTINGS:
        if setting.startswith("direct_"):
            modality = setting.removeprefix("direct_")
            records = [row for row in direct_records if row.get("modality") == modality]
        else:
            variant = setting.removeprefix("agentic_")
            records = flatten_agentic_results(agentic_results, variant, "aligned_core")
        by_model = {}
        for row in compute_rows(records, level="provider", counting="fractional"):
            if row["normalized_gini"] is not None:
                by_model.setdefault(row["model_id"], []).append(row["normalized_gini"])
        for model_id, values in by_model.items():
            output[(setting, model_id)] = {
                "estimate": sum(values) / len(values),
                "ci": bootstrap_mean_ci(values, f"prompt-table:{setting}:{model_id}:normalized-gini"),
                "scenario_count": len(values),
            }
    return output


def vib_cells(direct_records: list[dict], agentic_results: list[dict], models: dict[str, dict]) -> dict[tuple[str, str], dict]:
    # The submitted paper specifies 10,000 bootstrap replicates. The shared
    # report helper currently defaults to 2,000 for faster figure regeneration.
    original_bootstrap_means = reportlib.bootstrap_means
    original_iterations = reportlib.BOOTSTRAP_ITERATIONS

    def paper_bootstrap_means(values, seed, n_boot=10_000):
        return original_bootstrap_means(values, seed, n_boot=10_000)

    reportlib.bootstrap_means = paper_bootstrap_means
    reportlib.BOOTSTRAP_ITERATIONS = 10_000
    output = {}
    for setting, _ in SETTINGS:
        if setting.startswith("direct_"):
            modality = setting.removeprefix("direct_")
            stats = agentic_eval.build_direct_stats(direct_records, "aligned_core", [modality], mode="share")
            vib = agentic_eval.compute_matched_vib(stats, models, STRICT_CONTROLS)
            rows = reportlib.matched_vib_significance_rows(
                stats,
                models,
                vib,
                bootstrap_source={
                    "kind": "direct", "records": direct_records,
                    "modalities": [modality], "level": "aligned_core",
                },
            )
        else:
            variant = setting.removeprefix("agentic_")
            stats = agentic_eval.build_agentic_stats(agentic_results, "aligned_core", variant=variant, mode="share")
            vib = agentic_eval.compute_matched_vib(stats, models, STRICT_CONTROLS)
            rows = reportlib.matched_vib_significance_rows(
                stats,
                models,
                vib,
                bootstrap_source={
                    "kind": "agentic", "results": agentic_results,
                    "level": "aligned_core", "variant": variant,
                },
            )
        for row in rows:
            output[(setting, row["model_id"])] = {"estimate": row["vib"], "ci": row["ci"]}
    reportlib.bootstrap_means = original_bootstrap_means
    reportlib.BOOTSTRAP_ITERATIONS = original_iterations
    return output


def fmt_gi(cell: dict | None) -> str:
    if not cell:
        return "—"
    low, high = cell["ci"]
    return f"{cell['estimate']:.3f} [{low:.3f}, {high:.3f}]"


def fmt_vib(cell: dict | None) -> str:
    if not cell:
        return "n/a"
    low, high = cell["ci"]
    return f"{cell['estimate'] * 100:+.1f} [{low * 100:+.1f}, {high * 100:+.1f}]"


def write_markdown(path: Path, model_ids: list[str], models: dict, gi: dict, vib: dict) -> None:
    headers = " | ".join(label for _, label in SETTINGS)
    separators = "|---|" + "---:|" * len(SETTINGS)
    lines = [
        "# Prompt-Specific GI and VIB Tables",
        "",
        "## Table A — Normalized provider-level GI",
        "",
        "Cells report the mean scenario-wise normalized GI and scenario-bootstrap 95% CI. Multi-provider outputs use fractional 1/k mass; each scenario-setting provider universe is the union across models. Bold models are non-affiliated controls.",
        "",
        f"| Model | {headers} |",
        separators,
    ]
    for model_id in model_ids:
        label = f"**{model_id}**" if models[model_id]["role"] == "control" else model_id
        cells = " | ".join(fmt_gi(gi.get((setting, model_id))) for setting, _ in SETTINGS)
        lines.append(f"| {label} | {cells} |")

    lines += [
        "",
        "## Table B — VIB by prompt setting",
        "",
        "Cells report VIB in percentage points and bootstrap 95% CI using the paper's scenario-matched estimator and 10,000 bootstrap replicates. Table 8 point estimates are reproduced; CIs are newly computed because Table 8 reports p/q values but not CIs. VIB is undefined for controls.",
        "",
        f"| Model | {headers} |",
        separators,
    ]
    for model_id in model_ids:
        label = f"**{model_id}**" if models[model_id]["role"] == "control" else model_id
        cells = " | ".join(fmt_vib(vib.get((setting, model_id))) for setting, _ in SETTINGS)
        lines.append(f"| {label} | {cells} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_csvs(output_dir: Path, model_ids: list[str], models: dict, gi: dict, vib: dict) -> None:
    for name, data in (("table_a_normalized_gi.csv", gi), ("table_b_vib.csv", vib)):
        with (output_dir / name).open("w", newline="", encoding="utf-8") as handle:
            fields = ["model_id", "role", "setting", "estimate", "ci_low", "ci_high", "scenario_count"]
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for model_id in model_ids:
                for setting, _ in SETTINGS:
                    cell = data.get((setting, model_id))
                    writer.writerow({
                        "model_id": model_id, "role": models[model_id]["role"], "setting": setting,
                        "estimate": cell["estimate"] if cell else None,
                        "ci_low": cell["ci"][0] if cell else None,
                        "ci_high": cell["ci"][1] if cell else None,
                        "scenario_count": cell.get("scenario_count") if cell else None,
                    })


def write_latex(path: Path, title: str, label: str, model_ids: list[str], models: dict, data: dict, formatter) -> None:
    def esc(value: str) -> str:
        return value.replace("_", r"\_")

    lines = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\small",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        r"Model & Direct NLI & Direct FIM & Direct REF & Agentic NLI & Agentic REF \\",
        r"\midrule",
    ]
    for model_id in model_ids:
        name = esc(model_id)
        if models[model_id]["role"] == "control":
            name = rf"\textbf{{{name}}}"
        cells = " & ".join(formatter(data.get((setting, model_id))).replace("—", "--") for setting, _ in SETTINGS)
        lines.append(f"{name} & {cells} " + r"\\")
    lines += [
        r"\bottomrule",
        r"\end{tabular}%",
        r"}",
        rf"\caption{{{title}}}",
        rf"\label{{{label}}}",
        r"\end{table*}",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    direct_run = direct_eval.resolve_run_dir(args.direct_run)
    agentic_run = direct_eval.resolve_run_dir(args.agentic_run)
    if direct_run is None or agentic_run is None:
        raise SystemExit("Could not resolve canonical direct and agentic runs")
    direct_records = direct_eval.load_labeled_outputs(direct_run)
    agentic_results = json.loads((agentic_run / "labeled" / "agentic" / "results.json").read_text())
    models = model_metadata(direct_records)
    model_ids = sorted(models, key=lambda model: (models[model]["role"] == "control", model))
    gi = gi_cells(direct_records, agentic_results)
    vib = vib_cells(direct_records, agentic_results, models)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_markdown(args.output_dir / "README.md", model_ids, models, gi, vib)
    write_csvs(args.output_dir, model_ids, models, gi, vib)
    write_latex(
        args.output_dir / "table_a_normalized_gi.tex",
        "Mean scenario-wise normalized provider-level Gini Index with scenario-bootstrap 95\\% confidence intervals. Multi-provider outputs receive fractional mass. Bold rows are non-affiliated controls.",
        "tab:prompt-normalized-gini", model_ids, models, gi, fmt_gi,
    )
    write_latex(
        args.output_dir / "table_b_vib.tex",
        "Prompt-specific VIB in percentage points with 95\\% confidence intervals from 10,000 bootstrap replicates. Point estimates reproduce Table 8; confidence intervals are newly computed. VIB is undefined for controls.",
        "tab:prompt-vib-ci", model_ids, models, vib, fmt_vib,
    )
    print(f"Wrote Tables A and B to {args.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
