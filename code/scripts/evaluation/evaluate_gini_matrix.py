#!/usr/bin/env python3
"""Run provider-Gini analysis across all comparable VIBench prompt settings."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import evaluate as direct_eval  # noqa: E402
from evaluate_gini import (  # noqa: E402
    compute_rows,
    flatten_agentic_results,
    summarize,
    write_csv,
    write_plot,
)


SETTINGS = (
    ("direct_nli", "direct", "nli"),
    ("direct_fim", "direct", "fim"),
    ("direct_reference_open", "direct", "reference_open"),
    ("agentic_free", "agentic", "free"),
    ("agentic_informed", "agentic", "informed"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute Gini indices for all direct and agentic prompt settings.")
    parser.add_argument("--direct-run", default="direct/complete/full_5c")
    parser.add_argument("--agentic-run", default="agentic/complete/opencode_full_5c")
    parser.add_argument("--agentic-level", choices=("primary", "aligned_core"), default="aligned_core")
    parser.add_argument("--level", choices=("provider", "ecosystem"), default="provider")
    parser.add_argument("--counting", choices=("occurrence", "fractional"), default="occurrence")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/analysis/gini_all_prompts"))
    parser.add_argument("--no-plot", action="store_true")
    return parser.parse_args()


def write_summary_csv(path: Path, rows: list[dict]) -> None:
    fields = ["setting", "run_kind", "prompt_type", "agentic_level", "model_id", "scenario_count", "mean_gini", "median_gini", "mean_normalized_gini", "median_normalized_gini", "min_gini", "max_gini"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, summaries: list[dict], results: list[dict], args: argparse.Namespace) -> None:
    lines = [
        "# Gini Index Across Prompt Settings",
        "",
        "Paper-style scenario-wide provider universes are computed independently within each setting.",
        f"Agentic results use `{args.agentic_level}` components; multi-label counting is `{args.counting}`.",
        "Agentic `free` corresponds to NLI-style prompting and `informed` to Reference-Open-style prompting; there is no agentic FIM condition.",
        "",
        "## Setting-Level Results",
        "",
        "Raw GI has scenario-specific maximum `(n-1)/n`; normalized GI divides by this maximum and ranges from 0 to 1.",
        "",
        "| Setting | Valid / total | Mean GI | Median GI | Mean normalized | Median normalized | Min | Max |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for setting in (item[0] for item in SETTINGS):
        setting_rows = [row for row in results if row["setting"] == setting]
        values = [row["gini"] for row in setting_rows if row["gini"] is not None]
        normalized = [row["normalized_gini"] for row in setting_rows if row["normalized_gini"] is not None]
        lines.append(
            f"| {setting} | {len(values)} / {len(setting_rows)} | {statistics.fmean(values):.3f} | "
            f"{statistics.median(values):.3f} | {statistics.fmean(normalized):.3f} | {statistics.median(normalized):.3f} | "
            f"{min(values):.3f} | {max(values):.3f} |"
        )
    lines += [
        "",
        "## Model-Level Results",
        "",
        "| Setting | Model | Scenarios | Mean GI | Median GI | Mean normalized | Median normalized | Min | Max |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summaries:
        lines.append(
            f"| {row['setting']} | {row['model_id']} | {row['scenario_count']} | "
            f"{row['mean_gini']:.3f} | {row['median_gini']:.3f} | {row['mean_normalized_gini']:.3f} | "
            f"{row['median_normalized_gini']:.3f} | {row['min_gini']:.3f} | {row['max_gini']:.3f} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
def main() -> int:
    args = parse_args()
    direct_run = direct_eval.resolve_run_dir(args.direct_run)
    agentic_run = direct_eval.resolve_run_dir(args.agentic_run)
    if direct_run is None:
        raise SystemExit(f"Direct run not found: {args.direct_run}")
    if agentic_run is None:
        raise SystemExit(f"Agentic run not found: {args.agentic_run}")

    direct_records = direct_eval.load_labeled_outputs(direct_run)
    agentic_path = agentic_run / "labeled" / "agentic" / "results.json"
    if not agentic_path.exists():
        raise SystemExit(f"Agentic results not found: {agentic_path}")
    agentic_results = json.loads(agentic_path.read_text(encoding="utf-8"))

    args.output_dir.mkdir(parents=True, exist_ok=True)
    all_results = []
    all_summaries = []
    for setting, run_kind, prompt_type in SETTINGS:
        if run_kind == "direct":
            records = [record for record in direct_records if record.get("modality") == prompt_type]
        else:
            records = flatten_agentic_results(agentic_results, prompt_type, args.agentic_level)
        rows = compute_rows(records, level=args.level, counting=args.counting)
        setting_summaries = summarize(rows)
        for row in rows:
            all_results.append({"setting": setting, "run_kind": run_kind, "prompt_type": prompt_type, **row})
        for row in setting_summaries:
            all_summaries.append({
                "setting": setting,
                "run_kind": run_kind,
                "prompt_type": prompt_type,
                "agentic_level": args.agentic_level if run_kind == "agentic" else "",
                **row,
            })
        setting_dir = args.output_dir / setting
        setting_dir.mkdir(exist_ok=True)
        write_csv(setting_dir / "gini_by_scenario.csv", rows)
        if not args.no_plot:
            write_plot(setting_dir / "gini_boxplot.png", rows)

    payload = {
        "method": {
            "paper": "https://arxiv.org/abs/2501.07849",
            "direct_run": str(direct_run),
            "agentic_run": str(agentic_run),
            "agentic_level": args.agentic_level,
            "label_level": args.level,
            "counting": args.counting,
            "unknown_labels_excluded": True,
            "scenario_wide_union_per_setting": True,
        },
        "summary": all_summaries,
        "scenario_model_results": all_results,
    }
    (args.output_dir / "gini_results.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    write_summary_csv(args.output_dir / "gini_summary.csv", all_summaries)
    write_markdown(args.output_dir / "README.md", all_summaries, all_results, args)
    print(f"Wrote {len(all_results)} scenario-model rows across {len(SETTINGS)} settings to {args.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
