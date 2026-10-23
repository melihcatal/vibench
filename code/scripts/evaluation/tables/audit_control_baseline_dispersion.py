#!/usr/bin/env python3
"""Audit scenario-level sensitivity of VIB baselines to individual controls."""

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

import sys as _sys
from pathlib import Path as _Path
# The evaluation modules form one namespace, grouped into folders for
# readability only, so every group is importable from every other.
_EVAL_DIR = _Path(__file__).resolve().parents[1]
for _group in ("core", "gini", "tables", "baselines", "audit"):
    _sys.path.insert(0, str(_EVAL_DIR / _group))
import evaluate as direct_eval  # noqa: E402
import model_registry as registry  # noqa: E402
import evaluate_agentic as agentic_eval  # noqa: E402

_TABLES_DIR = Path(__file__).resolve().parents[4] / "outputs" / "tables"


CONTROLS = tuple(registry.strict_controls())
TARGETS = ("aws", "google", "microsoft_openai", "ibm", "alibaba")
SETTINGS = (
    ("direct_nli", "direct", "nli"),
    ("direct_fim", "direct", "fim"),
    ("direct_reference_open", "direct", "reference_open"),
    ("agentic_free", "agentic", "free"),
    ("agentic_informed", "agentic", "informed"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit control-model outliers in scenario-matched VIB baselines.")
    parser.add_argument("--direct-run", default="direct/complete/full_5c")
    parser.add_argument("--agentic-run", default="agentic/complete/opencode_full_5c")
    parser.add_argument("--output-dir", type=Path, default=_TABLES_DIR / "control_composition")
    return parser.parse_args()


def rate(stats, model: str, scenario: str, target: str) -> float | None:
    bucket = stats.get(model, {}).get(scenario)
    if not bucket or bucket["total"] <= 0:
        return None
    return bucket["counts"].get(target, 0.0) / bucket["total"]


def load_model_metadata(records: list[dict]) -> dict[str, dict]:
    models = {}
    for record in records:
        model_id = record.get("model_id")
        affiliation = (
            record.get("model_ecosystem_affiliation")
            or record.get("model_cloud_affiliation")
            or record.get("ecosystem_affiliation")
        )
        if model_id:
            models[model_id] = {
                "role": "affiliated" if affiliation else "control",
                "ecosystem_affiliation": affiliation,
                "cloud_affiliation": affiliation,
            }
    return models


def aggregate_model_vib(stats, model_id: str, affiliation: str, method: str) -> float:
    scenario_parts = []
    for scenario, bucket in stats.get(model_id, {}).items():
        if bucket["total"] <= 0:
            continue
        control_rates = []
        pooled_success = 0.0
        pooled_total = 0
        for control in CONTROLS:
            control_bucket = stats.get(control, {}).get(scenario)
            if not control_bucket or control_bucket["total"] <= 0:
                continue
            success = control_bucket["counts"].get(affiliation, 0.0)
            control_rates.append(success / control_bucket["total"])
            pooled_success += success
            pooled_total += control_bucket["total"]
        if not control_rates:
            continue
        if method == "mean":
            baseline = statistics.fmean(control_rates)
        elif method == "median":
            baseline = statistics.median(control_rates)
        elif method == "pooled":
            baseline = pooled_success / pooled_total
        else:
            raise ValueError(f"Unknown aggregation method: {method}")
        model_rate = bucket["counts"].get(affiliation, 0.0) / bucket["total"]
        scenario_parts.append((bucket["total"], model_rate - baseline))
    total = sum(count for count, _ in scenario_parts)
    return sum(count * delta for count, delta in scenario_parts) / total


def model_sensitivity_rows(direct_records: list[dict], agentic_results: list[dict], models: dict[str, dict]):
    settings = {
        "direct": agentic_eval.build_direct_stats(
            direct_records, "aligned_core", direct_eval.DIRECT_MODALITIES, mode="share"
        ),
        "agentic": agentic_eval.build_agentic_stats(agentic_results, "aligned_core", mode="share"),
    }
    aggregation_rows = []
    subset_output_rows = []
    for setting, stats in settings.items():
        subset_summary, _, _ = agentic_eval.compute_matched_vib_subset_robustness(stats, models)
        for model_id, info in sorted(models.items()):
            affiliation = info.get("ecosystem_affiliation")
            if info.get("role") != "affiliated" or not affiliation or model_id not in stats:
                continue
            estimates = {
                method: aggregate_model_vib(stats, model_id, affiliation, method)
                for method in ("mean", "pooled", "median")
            }
            aggregation_rows.append({
                "setting": setting,
                "model_id": model_id,
                "mean_vib": estimates["mean"],
                "pooled_vib": estimates["pooled"],
                "median_vib": estimates["median"],
                "pooled_minus_mean": estimates["pooled"] - estimates["mean"],
                "median_minus_mean": estimates["median"] - estimates["mean"],
            })
            summary = subset_summary[model_id]
            subset_output_rows.append({
                "setting": setting,
                "model_id": model_id,
                "strict_vib": summary["strict_vib"],
                "min_vib": summary["min_vib"],
                "median_vib": summary["median_vib"],
                "max_vib": summary["max_vib"],
                "positive_subsets": summary["positive_count"],
                "negative_subsets": summary["negative_count"],
                "subset_count": summary["subset_count"],
            })
    return aggregation_rows, subset_output_rows


def audit_rows(direct_records: list[dict], agentic_results: list[dict]) -> list[dict]:
    rows = []
    for setting, kind, prompt_type in SETTINGS:
        if kind == "direct":
            stats = agentic_eval.build_direct_stats(direct_records, "aligned_core", [prompt_type], mode="share")
        else:
            stats = agentic_eval.build_agentic_stats(
                agentic_results, "aligned_core", variant=prompt_type, mode="share"
            )
        scenarios = sorted({scenario for control in CONTROLS for scenario in stats.get(control, {})})
        for scenario in scenarios:
            for target in TARGETS:
                rates = {control: rate(stats, control, scenario, target) for control in CONTROLS}
                if any(value is None for value in rates.values()):
                    continue
                values = list(rates.values())
                baseline = statistics.fmean(values)
                leave_one_out = {
                    control: statistics.fmean(value for other, value in rates.items() if other != control)
                    for control in CONTROLS
                }
                changes = {control: abs(value - baseline) for control, value in leave_one_out.items()}
                most_influential = max(changes, key=changes.get)
                rows.append({
                    "setting": setting,
                    "scenario_id": scenario,
                    "target_ecosystem": target,
                    "deepseek_rate": rates[CONTROLS[0]],
                    "mistral_rate": rates[CONTROLS[1]],
                    "grok_rate": rates[CONTROLS[2]],
                    "mean_baseline": baseline,
                    "control_range": max(values) - min(values),
                    "max_leave_one_out_change": changes[most_influential],
                    "most_influential_control": most_influential,
                    "baseline_without_influential": leave_one_out[most_influential],
                })
    return rows


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def write_markdown(path: Path, rows: list[dict], aggregation_rows: list[dict], subset_rows: list[dict]) -> None:
    ranges = [row["control_range"] for row in rows]
    changes = [row["max_leave_one_out_change"] for row in rows]
    ordered_changes = sorted(changes)
    p90 = ordered_changes[int(0.9 * (len(ordered_changes) - 1))]
    active = [
        row for row in rows
        if row["deepseek_rate"] + row["mistral_rate"] + row["grok_rate"] > 0
    ]
    active_ranges = sorted(row["control_range"] for row in active)
    active_changes = sorted(row["max_leave_one_out_change"] for row in active)
    lines = [
        "# Control-Baseline Dispersion Audit",
        "",
        f"Audited `{len(rows)}` scenario × prompt-setting × target-ecosystem cells.",
        "Rates use the same share-normalized ecosystem attribution as VIB.",
        "",
        "## Panel A: Aggregation-Rule Sensitivity",
        "",
        "VIB values are percentage points. `Pooled` weights control generations directly; `Median` uses the scenario-specific median control rate.",
        "",
        "| Setting | Model | Mean | Pooled | Median | Pooled - Mean | Median - Mean |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in aggregation_rows:
        lines.append(
            f"| {row['setting']} | {row['model_id']} | {row['mean_vib']*100:+.2f} | "
            f"{row['pooled_vib']*100:+.2f} | {row['median_vib']*100:+.2f} | "
            f"{row['pooled_minus_mean']*100:+.2f} | {row['median_minus_mean']*100:+.2f} |"
        )
    lines += [
        "",
        "## Panel B: Exhaustive Control-Subset Sensitivity",
        "",
        "All seven non-empty subsets are included: three singleton controls, three control pairs, and all three controls.",
        "",
        "| Setting | Model | Strict | Min | Median | Max | Positive | Negative |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in subset_rows:
        lines.append(
            f"| {row['setting']} | {row['model_id']} | {row['strict_vib']*100:+.2f} | "
            f"{row['min_vib']*100:+.2f} | {row['median_vib']*100:+.2f} | {row['max_vib']*100:+.2f} | "
            f"{row['positive_subsets']}/{row['subset_count']} | {row['negative_subsets']}/{row['subset_count']} |"
        )
    lines += [
        "",
        "## Panel C: Scenario-Level Influence",
        "",
        f"- Median range across the three controls: **{pct(statistics.median(ranges))}**.",
        f"- Median maximum leave-one-out change in the mean baseline: **{pct(statistics.median(changes))}**.",
        f"- 90th percentile maximum leave-one-out change: **{pct(p90)}**.",
        f"- Maximum leave-one-out change: **{pct(max(changes))}**.",
        f"- Cells with leave-one-out change ≥5 pp: **{sum(value >= .05 for value in changes)}/{len(changes)}**.",
        f"- Cells with leave-one-out change ≥10 pp: **{sum(value >= .10 for value in changes)}/{len(changes)}**.",
        "",
        "Among cells where at least one control selects the target ecosystem:",
        f"- Active cells: **{len(active)}/{len(rows)}**.",
        f"- Median control range: **{pct(statistics.median(active_ranges))}**.",
        f"- Median maximum leave-one-out change: **{pct(statistics.median(active_changes))}**.",
        f"- Active cells with leave-one-out change ≥10 pp: **{sum(value >= .10 for value in active_changes)}/{len(active_changes)}**.",
        "",
        "### Most Sensitive Cells",
        "",
        "| Setting | Scenario | Target | DeepSeek | Mistral | Grok | Mean | Range | Max LOO change | Removed |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in sorted(rows, key=lambda item: item["max_leave_one_out_change"], reverse=True)[:20]:
        lines.append(
            f"| {row['setting']} | {row['scenario_id']} | {row['target_ecosystem']} | "
            f"{pct(row['deepseek_rate'])} | {pct(row['mistral_rate'])} | {pct(row['grok_rate'])} | "
            f"{pct(row['mean_baseline'])} | {pct(row['control_range'])} | "
            f"{pct(row['max_leave_one_out_change'])} | {row['most_influential_control']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    direct_run = direct_eval.resolve_run_dir(args.direct_run)
    agentic_run = direct_eval.resolve_run_dir(args.agentic_run)
    if direct_run is None or agentic_run is None:
        raise SystemExit("Could not resolve canonical runs")
    direct_records = direct_eval.load_labeled_outputs(direct_run)
    agentic_results = json.loads((agentic_run / "labeled" / "agentic" / "results.json").read_text())
    rows = audit_rows(direct_records, agentic_results)
    models = load_model_metadata(direct_records)
    aggregation_rows, subset_rows = model_sensitivity_rows(direct_records, agentic_results, models)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (args.output_dir / "control_baseline_dispersion.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    (args.output_dir / "control_baseline_dispersion.json").write_text(json.dumps(rows, indent=2) + "\n")
    for filename, output_rows in (
        ("aggregation_rule_sensitivity.csv", aggregation_rows),
        ("control_subset_sensitivity.csv", subset_rows),
    ):
        with (args.output_dir / filename).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(output_rows[0]))
            writer.writeheader()
            writer.writerows(output_rows)
    (args.output_dir / "baseline_sensitivity.json").write_text(
        json.dumps({"aggregation_rule": aggregation_rows, "control_subsets": subset_rows, "scenario_influence": rows}, indent=2) + "\n"
    )
    write_markdown(args.output_dir / "README.md", rows, aggregation_rows, subset_rows)
    print(f"Audited {len(rows)} cells; wrote results to {args.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
