#!/usr/bin/env python3
"""Recompute GPT VIB under alternative Microsoft/OpenAI affiliation mappings."""

from __future__ import annotations

import argparse
import copy
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import detect_services  # noqa: E402
import evaluate as direct_eval  # noqa: E402
import model_registry as registry  # noqa: E402
import evaluate_agentic as agentic_eval  # noqa: E402
import generate_vibench_results_markdown as reportlib  # noqa: E402
from generate_gini_vib_comparison import model_metadata  # noqa: E402


STRICT_CONTROLS = registry.strict_controls()
GPT_MODELS = ["gpt-5.4", "gpt-5.4-mini"]
MAPPINGS = {
    "merged_microsoft_openai": "microsoft_openai",
    "openai_only": "openai",
    "azure_only": "azure",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--direct-run", default="direct/complete/full_5c")
    parser.add_argument("--agentic-run", default="agentic/complete/opencode_full_5c")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/analysis/indirect_affiliation_sensitivity"),
    )
    parser.add_argument("--bootstrap-iterations", type=int, default=10_000)
    parser.add_argument("--bootstrap-seed", type=int, default=42)
    return parser.parse_args()


def category(provider: str, mapping: str) -> str:
    if provider == "openai":
        return "microsoft_openai" if mapping == "merged_microsoft_openai" else "openai"
    if provider in {"azure", "azure_openai"}:
        return "microsoft_openai" if mapping == "merged_microsoft_openai" else "azure"
    return detect_services.PROVIDER_TO_ECOSYSTEM.get(provider, provider)


def remap_labels(providers: list[str], mapping: str) -> list[str]:
    labels = []
    for provider in providers:
        label = category(provider, mapping)
        if label != "unknown" and label not in labels:
            labels.append(label)
    return labels


def remap_direct(records: list[dict], mapping: str) -> list[dict]:
    output = []
    for source in records:
        row = copy.copy(source)
        providers = row.get("detected_providers") or []
        if not providers and row.get("detected_provider") not in {None, "unknown"}:
            providers = [row["detected_provider"]]
        labels = remap_labels(providers, mapping)
        row["detected_ecosystems"] = labels
        row["detected_ecosystem"] = labels[0] if labels else "unknown"
        output.append(row)
    return output


def remap_agentic(results: list[dict], mapping: str) -> list[dict]:
    output = copy.deepcopy(results)
    for result in output:
        for component in (result.get("components") or {}).values():
            providers = component.get("detected_providers") or []
            if not providers and component.get("provider") not in {None, "unknown"}:
                providers = [component["provider"]]
            labels = remap_labels(providers, mapping)
            component["detected_ecosystems"] = labels
            component["ecosystem"] = labels[0] if labels else "unknown"
    return output


def direct_cluster_map(records: list[dict], model_id: str, target: str) -> dict[str, list[float]]:
    clusters = defaultdict(lambda: defaultdict(list))
    for row in records:
        if row.get("model_id") != model_id or row.get("modality") not in direct_eval.DIRECT_MODALITIES:
            continue
        if agentic_eval._task_suffix(row.get("task_id")) not in {"a", "b", "c", "d"}:
            continue
        scenario = row.get("scenario_id")
        cluster = (row.get("task_id"), row.get("modality"))
        clusters[scenario][cluster].append(
            direct_eval._record_target_share(row, target, field="detected_ecosystem")
        )
    return {
        scenario: [float(np.mean(values)) for values in grouped.values()]
        for scenario, grouped in clusters.items()
    }


def agentic_cluster_map(results: list[dict], model_id: str, target: str) -> dict[str, list[float]]:
    clusters = defaultdict(list)
    for row in results:
        if row.get("model_id") != model_id:
            continue
        values = [
            agentic_eval._affiliation_share(component, target) or 0.0
            for component in (row.get("components") or {}).values()
            if component.get("component_group") == "aligned_core"
        ]
        if values:
            scenario = row.get("primary_atomic_scenario") or "unknown"
            clusters[scenario].append(float(np.mean(values)))
    return dict(clusters)


def clustered_inference(
    source: list[dict],
    kind: str,
    model_id: str,
    target: str,
    scenario_rows: list[dict],
    point_estimate: float,
    key: tuple,
) -> dict:
    mapper = direct_cluster_map if kind == "direct" else agentic_cluster_map
    model_map = mapper(source, model_id, target)
    control_maps = {control: mapper(source, control, target) for control in STRICT_CONTROLS}
    n_boot = reportlib.BOOTSTRAP_ITERATIONS
    samples = np.zeros(n_boot, dtype=float)
    total_units = sum(row["target_total"] for row in scenario_rows)
    for scenario_row in scenario_rows:
        scenario = scenario_row["scenario_id"]
        model_clusters = model_map.get(scenario) or []
        available_controls = {
            control: values
            for control, scenario_map in control_maps.items()
            if (values := scenario_map.get(scenario))
        }
        if not model_clusters or not available_controls:
            continue
        model_boot = reportlib.bootstrap_means(
            model_clusters,
            reportlib.bootstrap_seed(*key, scenario, "model"),
        )
        control_boot = np.mean(
            np.vstack([
                reportlib.bootstrap_means(
                    values,
                    reportlib.bootstrap_seed(*key, scenario, control),
                )
                for control, values in sorted(available_controls.items())
            ]),
            axis=0,
        )
        samples += (scenario_row["target_total"] / total_units) * (model_boot - control_boot)
    return reportlib.bootstrap_stats_from_samples(samples, point_estimate)


def compute_rows(direct_records: list[dict], agentic_results: list[dict]) -> list[dict]:
    base_models = model_metadata(direct_records)
    rows = []
    for mapping, target in MAPPINGS.items():
        models = copy.deepcopy(base_models)
        for model_id in GPT_MODELS:
            models[model_id]["ecosystem_affiliation"] = target
            models[model_id]["cloud_affiliation"] = target

        mapped_direct = remap_direct(direct_records, mapping)
        direct_stats = agentic_eval.build_direct_stats(
            mapped_direct, "aligned_core", direct_eval.DIRECT_MODALITIES, mode="share"
        )
        direct_vib = agentic_eval.compute_matched_vib(direct_stats, models, STRICT_CONTROLS)

        mapped_agentic = remap_agentic(agentic_results, mapping)
        agentic_stats = agentic_eval.build_agentic_stats(mapped_agentic, "aligned_core", mode="share")
        agentic_vib = agentic_eval.compute_matched_vib(agentic_stats, models, STRICT_CONTROLS)

        for model_id in GPT_MODELS:
            for setting, values in (("direct", direct_vib), ("agentic", agentic_vib)):
                row = values.get(model_id)
                if not row:
                    continue
                inference = clustered_inference(
                    mapped_direct if setting == "direct" else mapped_agentic,
                    setting,
                    model_id,
                    target,
                    row["scenario_rows"],
                    row["vib"],
                    ("indirect_affiliation", mapping, setting, model_id, target),
                )
                rows.append({
                    "mapping": mapping,
                    "target": target,
                    "setting": setting,
                    "model_id": model_id,
                    "model_rate": row["model_rate"],
                    "control_rate": row["control_avg"],
                    "vib": row["vib"],
                    "ci_low": inference["ci"][0],
                    "ci_high": inference["ci"][1],
                    "p_value": inference["p_value"],
                    "units": row["units"],
                })
    return rows


def write_outputs(output_dir: Path, rows: list[dict]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fields = [
        "mapping", "target", "setting", "model_id", "model_rate", "control_rate", "vib",
        "ci_low", "ci_high", "p_value", "units",
    ]
    with (output_dir / "indirect_affiliation_sensitivity.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "indirect_affiliation_sensitivity.json").write_text(
        json.dumps(rows, indent=2) + "\n", encoding="utf-8"
    )

    lookup = {(row["mapping"], row["model_id"], row["setting"]): row for row in rows}
    lines = [
        "# Indirect-Affiliation Sensitivity",
        "",
        "Scenario-matched VIB in percentage points with 95% clustered bootstrap confidence intervals. Each mapping recomputes both the model rate and the strict-control baseline after re-normalizing multi-provider outputs.",
        "",
        "| Affiliation mapping | GPT-5.4 direct | GPT-5.4 Mini direct | GPT-5.4 agentic | GPT-5.4 Mini agentic |",
        "|---|---:|---:|---:|---:|",
    ]
    labels = {
        "merged_microsoft_openai": "Merged Microsoft/OpenAI (paper)",
        "openai_only": "OpenAI surfaces only",
        "azure_only": "Azure surfaces only",
    }
    for mapping in MAPPINGS:
        values = []
        for model_id, setting in (
            ("gpt-5.4", "direct"),
            ("gpt-5.4-mini", "direct"),
            ("gpt-5.4", "agentic"),
            ("gpt-5.4-mini", "agentic"),
        ):
            row = lookup[(mapping, model_id, setting)]
            values.append(
                f"{row['vib'] * 100:+.1f} ({row['ci_low'] * 100:+.1f}, {row['ci_high'] * 100:+.1f})"
            )
        lines.append(f"| {labels[mapping]} | " + " | ".join(values) + " |")
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    direct_run = direct_eval.resolve_run_dir(args.direct_run)
    agentic_run = direct_eval.resolve_run_dir(args.agentic_run)
    if direct_run is None or agentic_run is None:
        raise SystemExit("Could not resolve retained main runs")
    direct_records = direct_eval.load_labeled_outputs(direct_run)
    agentic_results = json.loads((agentic_run / "labeled" / "agentic" / "results.json").read_text())
    reportlib.BOOTSTRAP_ITERATIONS = args.bootstrap_iterations
    reportlib.BOOTSTRAP_SEED = args.bootstrap_seed
    rows = compute_rows(direct_records, agentic_results)
    write_outputs(args.output_dir, rows)
    print((args.output_dir / "README.md").resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
