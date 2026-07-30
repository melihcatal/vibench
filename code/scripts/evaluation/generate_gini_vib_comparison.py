#!/usr/bin/env python3
"""Generate per-model Gini/VIB comparison tables with bootstrap intervals."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import evaluate as direct_eval  # noqa: E402
import evaluate_agentic as agentic_eval  # noqa: E402
import generate_vibench_results_markdown as reportlib  # noqa: E402
from evaluate_gini import compute_rows  # noqa: E402


STRICT_CONTROLS = ["deepseek-v3.2", "mistral-large-3", "grok-4-1-fast-reasoning"]
BOOTSTRAP_ITERATIONS = 2000
BOOTSTRAP_SEED = 42


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare per-model ecosystem Gini and VIB with bootstrap CIs.")
    parser.add_argument("--direct-run", default="direct/complete/full_5c")
    parser.add_argument("--agentic-run", default="agentic/complete/opencode_full_5c")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/analysis/gini_vib_per_model"))
    return parser.parse_args()


def model_metadata(direct_records: list[dict]) -> dict[str, dict]:
    models = {}
    for record in direct_records:
        model_id = record.get("model_id")
        if not model_id:
            continue
        affiliation = (
            record.get("model_ecosystem_affiliation")
            or record.get("model_cloud_affiliation")
            or record.get("ecosystem_affiliation")
        )
        models[model_id] = {
            "role": "affiliated" if affiliation else "control",
            "ecosystem_affiliation": affiliation,
            "cloud_affiliation": affiliation,
        }
    return models


def flatten_agentic(results: list[dict]) -> list[dict]:
    records = []
    for result in results:
        for component in (result.get("components") or {}).values():
            if component.get("component_group") != "aligned_core":
                continue
            records.append({
                "model_id": result.get("model_id"),
                "scenario_id": component.get("atomic_scenario") or result.get("primary_atomic_scenario"),
                "detected_ecosystems": component.get("detected_ecosystems") or [],
            })
    return records


def bootstrap_mean_ci(values: list[float], key: str) -> tuple[float, float]:
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    seed = (BOOTSTRAP_SEED + int.from_bytes(digest[:8], "big")) % (2**63 - 1)
    array = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(array), size=(BOOTSTRAP_ITERATIONS, len(array)))
    means = array[indices].mean(axis=1)
    low, high = np.quantile(means, [0.025, 0.975])
    return float(low), float(high)


def gini_summaries(records: list[dict], setting: str) -> dict[str, dict]:
    by_model: dict[str, list[dict]] = defaultdict(list)
    for row in compute_rows(records, level="ecosystem", counting="occurrence"):
        if row["gini"] is not None:
            by_model[row["model_id"]].append(row)
    output = {}
    for model_id, rows in sorted(by_model.items()):
        raw = [row["gini"] for row in rows]
        normalized = [row["normalized_gini"] for row in rows]
        output[model_id] = {
            "scenario_count": len(rows),
            "mean_gini": float(np.mean(raw)),
            "gini_ci": bootstrap_mean_ci(raw, f"{setting}:{model_id}:raw"),
            "mean_normalized_gini": float(np.mean(normalized)),
            "normalized_gini_ci": bootstrap_mean_ci(normalized, f"{setting}:{model_id}:normalized"),
        }
    return output


def vib_summaries(
    direct_records: list[dict],
    agentic_results: list[dict],
    models: dict[str, dict],
) -> dict[str, dict[str, dict]]:
    direct_stats = agentic_eval.build_direct_stats(
        direct_records, "aligned_core", direct_eval.DIRECT_MODALITIES, mode="share"
    )
    direct_vib = agentic_eval.compute_matched_vib(direct_stats, models, STRICT_CONTROLS)
    direct_rows = reportlib.matched_vib_significance_rows(
        direct_stats,
        models,
        direct_vib,
        bootstrap_source={
            "kind": "direct",
            "records": direct_records,
            "modalities": direct_eval.DIRECT_MODALITIES,
            "level": "aligned_core",
        },
    )

    agentic_stats = agentic_eval.build_agentic_stats(agentic_results, "aligned_core", mode="share")
    agentic_vib = agentic_eval.compute_matched_vib(agentic_stats, models, STRICT_CONTROLS)
    agentic_rows = reportlib.matched_vib_significance_rows(
        agentic_stats,
        models,
        agentic_vib,
        bootstrap_source={"kind": "agentic", "results": agentic_results, "level": "aligned_core"},
    )
    return {
        "direct": {row["model_id"]: row for row in direct_rows},
        "agentic": {row["model_id"]: row for row in agentic_rows},
    }


def combined_rows(
    setting: str,
    gini: dict[str, dict],
    vib: dict[str, dict],
    models: dict[str, dict],
) -> list[dict]:
    rows = []
    for model_id, gini_row in sorted(gini.items()):
        vib_row = vib.get(model_id)
        rows.append({
            "setting": setting,
            "model_id": model_id,
            "role": models.get(model_id, {}).get("role", "unknown"),
            "affiliation": models.get(model_id, {}).get("ecosystem_affiliation"),
            "scenario_count": gini_row["scenario_count"],
            "vib": vib_row.get("vib") if vib_row else None,
            "vib_ci": vib_row.get("ci") if vib_row else None,
            **gini_row,
        })
    return rows


def fmt_ci(value: float | None, ci: tuple[float, float] | None, scale: float = 1.0) -> str:
    if value is None or ci is None:
        return "n/a"
    return f"{value * scale:.3f} [{ci[0] * scale:.3f}, {ci[1] * scale:.3f}]"


def write_markdown(path: Path, rows: list[dict]) -> None:
    lines = [
        "# Per-Model Gini and VIB",
        "",
        "Values are point estimates with 95% bootstrap confidence intervals. GI is computed at ecosystem level and averaged over scenarios; its CI resamples scenarios. VIB uses the paper's scenario-matched response bootstrap. Control-model VIB is undefined by design.",
    ]
    for setting in ("direct", "agentic"):
        lines += [
            "",
            f"## {setting.title()}",
            "",
            "| Model | Role | Affiliation | Scenarios | VIB pp [95% CI] | Mean GI [95% CI] | Mean normalized GI [95% CI] |",
            "|---|---|---|---:|---:|---:|---:|",
        ]
        for row in rows:
            if row["setting"] != setting:
                continue
            lines.append(
                f"| {row['model_id']} | {row['role']} | {row['affiliation'] or 'n/a'} | {row['scenario_count']} | "
                f"{fmt_ci(row['vib'], row['vib_ci'], 100)} | {fmt_ci(row['mean_gini'], row['gini_ci'])} | "
                f"{fmt_ci(row['mean_normalized_gini'], row['normalized_gini_ci'])} |"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = [
        "setting", "model_id", "role", "affiliation", "scenario_count", "vib", "vib_ci_low", "vib_ci_high",
        "mean_gini", "gini_ci_low", "gini_ci_high", "mean_normalized_gini", "normalized_gini_ci_low", "normalized_gini_ci_high",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            output = {key: row.get(key) for key in fields}
            for source, low, high in (
                ("vib_ci", "vib_ci_low", "vib_ci_high"),
                ("gini_ci", "gini_ci_low", "gini_ci_high"),
                ("normalized_gini_ci", "normalized_gini_ci_low", "normalized_gini_ci_high"),
            ):
                ci = row.get(source)
                output[low] = ci[0] if ci else None
                output[high] = ci[1] if ci else None
            writer.writerow(output)


def main() -> int:
    args = parse_args()
    direct_run = direct_eval.resolve_run_dir(args.direct_run)
    agentic_run = direct_eval.resolve_run_dir(args.agentic_run)
    if direct_run is None or agentic_run is None:
        raise SystemExit("Could not resolve direct and agentic runs")
    direct_records = direct_eval.load_labeled_outputs(direct_run)
    agentic_results = json.loads((agentic_run / "labeled" / "agentic" / "results.json").read_text())
    models = model_metadata(direct_records)
    vib = vib_summaries(direct_records, agentic_results, models)
    rows = combined_rows("direct", gini_summaries(direct_records, "direct"), vib["direct"], models)
    rows += combined_rows("agentic", gini_summaries(flatten_agentic(agentic_results), "agentic"), vib["agentic"], models)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_markdown(args.output_dir / "README.md", rows)
    write_csv(args.output_dir / "gini_vib_per_model.csv", rows)
    (args.output_dir / "gini_vib_per_model.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} model-setting rows to {args.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
