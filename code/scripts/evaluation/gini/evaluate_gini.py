#!/usr/bin/env python3
"""Compute paper-style provider Gini indices for VIBench direct results.

The metric follows Zhang et al., "The Invisible Hand" (arXiv:2501.07849):
for each scenario, the category universe is the union of providers observed in
all model responses. Each model is then scored over that same, zero-filled
universe.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

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


def gini(values: Iterable[float]) -> float | None:
    """Return the Gini coefficient, or None for an empty/all-zero vector."""
    ordered = sorted(float(value) for value in values)
    if any(value < 0 for value in ordered):
        raise ValueError("Gini values must be non-negative")
    total = sum(ordered)
    if not ordered or total == 0:
        return None
    n = len(ordered)
    return sum((2 * index - n - 1) * value for index, value in enumerate(ordered, 1)) / (n * total)


def record_labels(record: dict, level: str) -> list[str]:
    plural = f"detected_{level}s"
    singular = f"detected_{level}"
    raw = record.get(plural)
    if isinstance(raw, list):
        labels = raw
    elif raw:
        labels = [raw]
    elif record.get(singular):
        labels = [record[singular]]
    else:
        labels = []
    return list(dict.fromkeys(str(label) for label in labels if label and label != "unknown"))


def compute_rows(records: list[dict], level: str = "provider", counting: str = "occurrence") -> list[dict]:
    counts: dict[tuple[str, str], Counter] = defaultdict(Counter)
    response_counts: Counter = Counter()
    valid_response_counts: Counter = Counter()
    scenario_universes: dict[str, set[str]] = defaultdict(set)

    for record in records:
        model = record.get("model_id") or record.get("model")
        scenario = record.get("scenario_id")
        if not model or not scenario:
            continue
        key = (scenario, model)
        response_counts[key] += 1
        labels = record_labels(record, level)
        if not labels:
            continue
        valid_response_counts[key] += 1
        weight = 1.0 / len(labels) if counting == "fractional" else 1.0
        for label in labels:
            counts[key][label] += weight
            scenario_universes[scenario].add(label)

    rows = []
    for scenario, model in sorted(response_counts):
        universe = sorted(scenario_universes[scenario])
        vector = [counts[(scenario, model)][label] for label in universe]
        score = gini(vector)
        max_score = (len(universe) - 1) / len(universe) if universe else None
        rows.append({
            "scenario_id": scenario,
            "model_id": model,
            "gini": score,
            "max_reachable_gini": max_score,
            "normalized_gini": score / max_score if score is not None and max_score else None,
            "provider_universe_size": len(universe),
            "provider_universe": universe,
            "counts": {label: counts[(scenario, model)][label] for label in universe},
            "response_count": response_counts[(scenario, model)],
            "labeled_response_count": valid_response_counts[(scenario, model)],
        })
    return rows


def summarize(rows: list[dict]) -> list[dict]:
    by_model: dict[str, list[float]] = defaultdict(list)
    normalized_by_model: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        if row["gini"] is not None:
            by_model[row["model_id"]].append(row["gini"])
        if row["normalized_gini"] is not None:
            normalized_by_model[row["model_id"]].append(row["normalized_gini"])
    summaries = []
    for model, values in sorted(by_model.items()):
        summaries.append({
            "model_id": model,
            "scenario_count": len(values),
            "mean_gini": statistics.fmean(values),
            "median_gini": statistics.median(values),
            "min_gini": min(values),
            "max_gini": max(values),
            "mean_normalized_gini": statistics.fmean(normalized_by_model[model]),
            "median_normalized_gini": statistics.median(normalized_by_model[model]),
        })
    return summaries


def flatten_agentic_results(results: list[dict], variant: str, level: str = "aligned_core") -> list[dict]:
    """Convert agentic result components into direct-like provider records."""
    records = []
    for result in results:
        if result.get("variant") != variant:
            continue
        if level == "primary":
            records.append({
                "model_id": result.get("model_id"),
                "scenario_id": result.get("primary_atomic_scenario"),
                "detected_providers": result.get("primary_providers") or [],
                "detected_ecosystems": result.get("primary_ecosystems") or [],
            })
            continue
        for component in (result.get("components") or {}).values():
            if component.get("component_group") != "aligned_core":
                continue
            records.append({
                "model_id": result.get("model_id"),
                "scenario_id": component.get("atomic_scenario") or result.get("primary_atomic_scenario"),
                "detected_providers": component.get("detected_providers") or [],
                "detected_ecosystems": component.get("detected_ecosystems") or [],
            })
    return records


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = ["scenario_id", "model_id", "gini", "max_reachable_gini", "normalized_gini", "provider_universe_size", "provider_universe", "counts", "response_count", "labeled_response_count"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            output = dict(row)
            output["provider_universe"] = json.dumps(output["provider_universe"], separators=(",", ":"))
            output["counts"] = json.dumps(output["counts"], separators=(",", ":"), sort_keys=True)
            writer.writerow(output)


def write_markdown(path: Path, summaries: list[dict], args: argparse.Namespace) -> None:
    lines = [
        "# Provider Gini Index",
        "",
        f"Run: `{args.run}`; modality: `{args.modality}`; level: `{args.level}`; counting: `{args.counting}`.",
        "The provider universe is the scenario-wide union across all models, matching arXiv:2501.07849.",
        "",
        "For a scenario with `n` providers, raw GI ranges from `0` to `(n-1)/n`; normalized GI divides by that attainable maximum.",
        "",
        "| Model | Scenarios | Mean GI | Median GI | Mean normalized GI | Median normalized GI | Min | Max |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summaries:
        lines.append(
            f"| {row['model_id']} | {row['scenario_count']} | {row['mean_gini']:.3f} | "
            f"{row['median_gini']:.3f} | {row['mean_normalized_gini']:.3f} | {row['median_normalized_gini']:.3f} | "
            f"{row['min_gini']:.3f} | {row['max_gini']:.3f} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_plot(path: Path, rows: list[dict]) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("matplotlib is required unless --no-plot is used") from exc
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        if row["gini"] is not None:
            grouped[row["model_id"]].append(row["gini"])
    models = sorted(grouped)
    width = max(9, len(models) * 0.85)
    fig, ax = plt.subplots(figsize=(width, 5.5))
    ax.boxplot([grouped[model] for model in models], tick_labels=models, showmeans=True)
    ax.set_ylabel("Gini index")
    ax.set_ylim(0, 1)
    ax.grid(axis="y", alpha=0.25)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute paper-style Gini indices from labeled VIBench outputs.")
    parser.add_argument("--run", default="direct/complete/full_5c", help="Direct run id or directory")
    parser.add_argument("--modality", default="nli", help="Direct modality to analyze (default: nli)")
    parser.add_argument("--level", choices=("provider", "ecosystem"), default="provider")
    parser.add_argument("--counting", choices=("occurrence", "fractional"), default="occurrence")
    parser.add_argument("--output-dir", type=Path, help="Output directory (default: RUN/analysis/gini_MODality)")
    parser.add_argument("--no-plot", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = direct_eval.resolve_run_dir(args.run)
    if run_dir is None:
        raise SystemExit(f"Run not found: {args.run}")
    records = [record for record in direct_eval.load_labeled_outputs(run_dir) if record.get("modality") == args.modality]
    if not records:
        raise SystemExit(f"No labeled records found for modality '{args.modality}' in {run_dir}")
    rows = compute_rows(records, level=args.level, counting=args.counting)
    if not any(row["gini"] is not None for row in rows):
        raise SystemExit("No detected labels were available for Gini calculation")
    summaries = summarize(rows)
    output_dir = args.output_dir or run_dir / "analysis" / f"gini_{args.modality}_{args.level}"
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "method": {
            "paper": "https://arxiv.org/abs/2501.07849",
            "run": str(run_dir),
            "modality": args.modality,
            "level": args.level,
            "counting": args.counting,
            "unknown_labels_excluded": True,
            "scenario_wide_union": True,
        },
        "summary": summaries,
        "scenario_model_results": rows,
    }
    (output_dir / "gini_results.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    write_csv(output_dir / "gini_by_scenario.csv", rows)
    write_markdown(output_dir / "README.md", summaries, args)
    if not args.no_plot:
        write_plot(output_dir / "gini_boxplot.png", rows)
    print(f"Analyzed {len(records)} responses; wrote {len(rows)} scenario-model rows to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
