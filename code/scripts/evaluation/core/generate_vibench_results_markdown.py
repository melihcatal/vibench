#!/usr/bin/env python3
"""
Generate a consolidated current-benchmark results markdown report.

The report includes:
- Raw direct ecosystem rates for all models
- Raw agentic summary metrics for all models
- Direct VIB with significance tests
- Agentic primary/aligned VIB with significance tests
- Direct -> agentic transition tests
- Agentic downstream-leakage tests
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import evaluate as direct_eval  # noqa: E402
import model_registry as registry  # noqa: E402
import evaluate_agentic as agentic_eval  # noqa: E402


STRICT_CONTROL_IDS = registry.strict_controls()
DOWNSTREAM_LEAKAGE_EXPECTATIONS = {
    "independent_expected",
    "compatible_but_independent",
}

DIRECT_ECOSYSTEM_COLUMNS = [
    "aws",
    "google",
    "microsoft_openai",
    "ibm",
    "alibaba",
    "independent",
    "anthropic",
    "unknown",
]

BOOTSTRAP_ITERATIONS = 10000
BOOTSTRAP_SEED = 42


def pct(value: float | None, digits: int = 1) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.{digits}f}%"


def fmt_p(value: float | None) -> str:
    if value is None:
        return "n/a"
    if value < 1e-4:
        return f"{value:.2e}"
    return f"{value:.4f}"


def fmt_delta(value: float | None, digits: int = 1) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:+.{digits}f}pp"


def fmt_ci(ci: tuple[float, float] | None, digits: int = 1) -> str:
    if ci is None:
        return "n/a"
    low, high = ci
    return f"[{low * 100:+.{digits}f}, {high * 100:+.{digits}f}]pp"


def fmt_mass(value: float | None) -> str:
    if value is None:
        return "n/a"
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.1f}"


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def diff_prop_stats(success_a: int, total_a: int, success_b: int, total_b: int):
    if total_a <= 0 or total_b <= 0:
        return {
            "rate_a": None,
            "rate_b": None,
            "delta": None,
            "ci": None,
            "p_value": None,
            "z": None,
        }
    rate_a = success_a / total_a
    rate_b = success_b / total_b
    delta = rate_a - rate_b
    se = math.sqrt(
        (rate_a * (1 - rate_a) / total_a) +
        (rate_b * (1 - rate_b) / total_b)
    )
    if se == 0:
        z = math.inf if delta != 0 else 0.0
        p_value = 0.0 if delta != 0 else 1.0
        ci = (delta, delta)
    else:
        z = delta / se
        p_value = 2 * (1 - normal_cdf(abs(z)))
        ci = (delta - 1.96 * se, delta + 1.96 * se)
    return {
        "rate_a": rate_a,
        "rate_b": rate_b,
        "delta": delta,
        "ci": ci,
        "p_value": p_value,
        "z": z,
    }


def normal_stats_from_delta_se(delta: float | None, se: float | None):
    if delta is None or se is None:
        return {"ci": None, "p_value": None, "z": None}
    if se == 0:
        z = math.inf if delta != 0 else 0.0
        p_value = 0.0 if delta != 0 else 1.0
        ci = (delta, delta)
    else:
        z = delta / se
        p_value = 2 * (1 - normal_cdf(abs(z)))
        ci = (delta - 1.96 * se, delta + 1.96 * se)
    return {
        "ci": ci,
        "p_value": p_value,
        "z": z,
    }


def bootstrap_seed(*parts) -> int:
    payload = "::".join(str(part) for part in parts)
    digest = hashlib.sha256(payload.encode("utf-8")).digest()
    return (BOOTSTRAP_SEED + int.from_bytes(digest[:8], "big")) % (2**63 - 1)


def bootstrap_means(values, seed: int, n_boot: int = BOOTSTRAP_ITERATIONS):
    arr = np.asarray(list(values), dtype=float)
    if arr.size == 0:
        return None
    if arr.size == 1:
        return np.repeat(arr[0], n_boot)
    rng = np.random.default_rng(seed)
    sample_idx = rng.integers(0, arr.size, size=(n_boot, arr.size))
    return arr[sample_idx].mean(axis=1)


def bootstrap_cluster_rates(units, seed: int, n_boot: int = BOOTSTRAP_ITERATIONS):
    if not units:
        return None
    successes = np.asarray([unit["success"] for unit in units], dtype=float)
    totals = np.asarray([unit["total"] for unit in units], dtype=float)
    if successes.size == 0:
        return None
    if successes.size == 1:
        return np.repeat(successes[0] / totals[0], n_boot)
    rng = np.random.default_rng(seed)
    sample_idx = rng.integers(0, successes.size, size=(n_boot, successes.size))
    sampled_success = successes[sample_idx].sum(axis=1)
    sampled_total = totals[sample_idx].sum(axis=1)
    return sampled_success / sampled_total


def cluster_unit(success: float, total: int) -> dict[str, float | int]:
    return {"success": float(success), "total": int(total)}


def bootstrap_stats_from_samples(samples, point_estimate: float | None):
    if samples is None:
        return {
            "ci": None,
            "p_value": None,
            "significant": None,
            "samples": None,
        }
    arr = np.asarray(samples, dtype=float)
    low, high = np.quantile(arr, [0.025, 0.975])
    nonneg = (np.sum(arr >= 0) + 1) / (arr.size + 1)
    nonpos = (np.sum(arr <= 0) + 1) / (arr.size + 1)
    p_value = min(1.0, 2 * min(nonneg, nonpos))
    significant = (low > 0) or (high < 0)
    return {
        "ci": (float(low), float(high)),
        "p_value": float(p_value),
        "significant": significant,
        "samples": arr,
        "point_estimate": point_estimate,
    }


def bootstrap_mean_from_unit_list(values, key, point_estimate):
    if not values:
        return {
            "ci": None,
            "p_value": None,
            "significant": None,
            "samples": None,
        }
    samples = bootstrap_means(values, bootstrap_seed(key, "mean"))
    return bootstrap_stats_from_samples(samples, point_estimate)


def bh_adjust(rows, key="p_value", out_key="q_value"):
    indexed = [(idx, row[key]) for idx, row in enumerate(rows) if row.get(key) is not None]
    if not indexed:
        return
    indexed.sort(key=lambda item: item[1])
    m = len(indexed)
    adjusted = [None] * len(rows)
    prev = 1.0
    for rank, (idx, p_value) in reversed(list(enumerate(indexed, start=1))):
        q_value = min(prev, p_value * m / rank)
        adjusted[idx] = q_value
        prev = q_value
    for idx, row in enumerate(rows):
        row[out_key] = adjusted[idx]


def ecosystem_label(value: str | None) -> str:
    return direct_eval._display_label(value)


def load_agentic_results(run_dir: Path):
    results_path = run_dir / "labeled" / "agentic" / "results.json"
    with open(results_path) as f:
        return json.load(f)


def pool_counts_from_stats(stats, model_ids, scenario_ids, target_ecosystem):
    selected = 0
    total = 0
    for model_id in model_ids:
        for scenario_id in scenario_ids:
            bucket = stats.get(model_id, {}).get(scenario_id)
            if not bucket or bucket["total"] <= 0:
                continue
            total += bucket["total"]
            selected += bucket["counts"].get(target_ecosystem, 0)
    return selected, total


def leakage_counts_for_model(rows, allowed_expectations=DOWNSTREAM_LEAKAGE_EXPECTATIONS):
    follows = 0.0
    total = 0
    for row in rows:
        primary_role = row.get("primary_component_role")
        primary_component = row.get("components", {}).get(primary_role)
        if not row.get("primary_present") or not primary_component:
            continue
        for comp in row.get("components", {}).values():
            if not comp.get("is_scored") or not comp.get("present"):
                continue
            if comp.get("coupling_expectation") not in allowed_expectations:
                continue
            overlap = agentic_eval._component_overlap_score(primary_component, comp)
            if overlap is None:
                continue
            total += 1
            follows += overlap
    return follows, total


def primary_share_map(row):
    ecosystems = row.get("primary_ecosystems") or [row.get("primary_ecosystem") or "unknown"]
    weight = 1.0 / len(ecosystems) if ecosystems else 1.0
    shares = Counter()
    for ecosystem in ecosystems:
        shares[ecosystem] += weight
    return shares


def top_primary_ecosystems(rows, k=3):
    counts = Counter()
    for row in rows:
        ecosystems = row.get("primary_ecosystems") or [row.get("primary_ecosystem") or "unknown"]
        weight = 1.0 / len(ecosystems) if ecosystems else 1.0
        for ecosystem in ecosystems:
            counts[ecosystem] += weight
    total = sum(counts.values()) or 1
    pieces = []
    for eco, count in counts.most_common(k):
        pieces.append(f"{ecosystem_label(eco)} {count/total:.0%}")
    return ", ".join(pieces)


def model_role(info):
    return info.get("role", "unknown")


def affiliated_model_ids(models_info, model_ids=None):
    allowed = set(model_ids) if model_ids is not None else None
    selected = []
    for model_id, info in sorted(models_info.items()):
        if info.get("role") != "affiliated":
            continue
        if allowed is not None and model_id not in allowed:
            continue
        affiliation = info.get("ecosystem_affiliation") or info.get("cloud_affiliation")
        if affiliation:
            selected.append(model_id)
    return selected


def direct_target_units(records, model_ids, target_ecosystem, modalities=None, level=None):
    allowed_modalities = set(modalities) if modalities is not None else None
    values = []
    for record in records:
        if record.get("model_id") not in model_ids:
            continue
        if allowed_modalities is not None and record.get("modality") not in allowed_modalities:
            continue
        suffix = agentic_eval._task_suffix(record.get("task_id"))
        if level == "primary" and suffix != "a":
            continue
        if level == "aligned_core" and suffix not in {"a", "b", "c", "d"}:
            continue
        values.append(direct_eval._record_target_share(record, target_ecosystem, field="detected_ecosystem"))
    return values


def direct_target_units_by_scenario(records, model_id, target_ecosystem, modalities, level):
    allowed_modalities = set(modalities)
    buckets = defaultdict(list)
    for record in records:
        if record.get("model_id") != model_id:
            continue
        if record.get("modality") not in allowed_modalities:
            continue
        scenario_id = record.get("scenario_id")
        if not scenario_id:
            continue
        suffix = agentic_eval._task_suffix(record.get("task_id"))
        if level == "primary" and suffix != "a":
            continue
        if level == "aligned_core" and suffix not in {"a", "b", "c", "d"}:
            continue
        buckets[scenario_id].append(
            direct_eval._record_target_share(record, target_ecosystem, field="detected_ecosystem")
        )
    return buckets


def direct_target_clusters_by_scenario(records, model_id, target_ecosystem, modalities, level):
    allowed_modalities = set(modalities)
    grouped = defaultdict(lambda: defaultdict(list))
    for record in records:
        if record.get("model_id") != model_id:
            continue
        if record.get("modality") not in allowed_modalities:
            continue
        scenario_id = record.get("scenario_id")
        if not scenario_id:
            continue
        suffix = agentic_eval._task_suffix(record.get("task_id"))
        if level == "primary" and suffix != "a":
            continue
        if level == "aligned_core" and suffix not in {"a", "b", "c", "d"}:
            continue
        cluster_key = (
            scenario_id,
            record.get("task_id"),
            record.get("modality"),
        )
        grouped[scenario_id][cluster_key].append(record)

    buckets = defaultdict(list)
    for scenario_id, clusters in grouped.items():
        for cluster_records in clusters.values():
            values = [
                direct_eval._record_target_share(record, target_ecosystem, field="detected_ecosystem")
                for record in cluster_records
            ]
            if values:
                buckets[scenario_id].append(cluster_unit(sum(values), len(values)))
    return buckets


def agentic_target_units_by_scenario(agentic_results, model_id, target_ecosystem, level, variant=None):
    buckets = defaultdict(list)
    for row in agentic_results:
        if row.get("model_id") != model_id:
            continue
        if variant and row.get("variant") != variant:
            continue
        scenario_id = row.get("primary_atomic_scenario") or "unknown"
        if level == "primary":
            component = row.get("components", {}).get(row.get("primary_component_role"), {})
            buckets[scenario_id].append(agentic_eval._affiliation_share(component, target_ecosystem) or 0.0)
            continue
        if level != "aligned_core":
            raise ValueError(f"Unsupported agentic level for bootstrap: {level}")
        for component in row.get("components", {}).values():
            if component.get("component_group") != "aligned_core":
                continue
            buckets[scenario_id].append(agentic_eval._affiliation_share(component, target_ecosystem) or 0.0)
    return buckets


def agentic_target_clusters_by_scenario(agentic_results, model_id, target_ecosystem, level, variant=None):
    buckets = defaultdict(list)
    for row in agentic_results:
        if row.get("model_id") != model_id:
            continue
        if variant and row.get("variant") != variant:
            continue
        scenario_id = row.get("primary_atomic_scenario") or "unknown"
        if level == "primary":
            component = row.get("components", {}).get(row.get("primary_component_role"), {})
            buckets[scenario_id].append(cluster_unit(agentic_eval._affiliation_share(component, target_ecosystem) or 0.0, 1))
            continue
        if level != "aligned_core":
            raise ValueError(f"Unsupported agentic level for bootstrap: {level}")
        values = []
        for component in row.get("components", {}).values():
            if component.get("component_group") != "aligned_core":
                continue
            values.append(agentic_eval._affiliation_share(component, target_ecosystem) or 0.0)
        if values:
            buckets[scenario_id].append(cluster_unit(sum(values), len(values)))
    return buckets


def agentic_target_units(agentic_results, model_ids, target_ecosystem, level="aligned_core", variant=None):
    values = []
    for model_id in model_ids:
        for scenario_values in agentic_target_units_by_scenario(
            agentic_results,
            model_id,
            target_ecosystem,
            level=level,
            variant=variant,
        ).values():
            values.extend(scenario_values)
    return values


def direct_affiliation_summary(records, models_info, modalities=None, model_ids=None):
    by_model_units = {}
    pooled_units = []
    for model_id in affiliated_model_ids(models_info, model_ids=model_ids):
        affiliation = models_info[model_id].get("ecosystem_affiliation") or models_info[model_id].get("cloud_affiliation")
        units = direct_target_units(records, [model_id], affiliation, modalities=modalities)
        if not units:
            continue
        by_model_units[model_id] = [float(v) for v in units]
        pooled_units.extend(by_model_units[model_id])

    by_model = {}
    for model_id, units in by_model_units.items():
        point = float(np.mean(units)) if units else None
        by_model[model_id] = {
            "rate": point,
            "n": len(units),
            "units": units,
            **bootstrap_mean_from_unit_list(units, ("direct_affiliation", tuple(modalities or ()), model_id), point),
        }

    point = float(np.mean(pooled_units)) if pooled_units else None
    return {
        "rate": point,
        "n": len(pooled_units),
        "units": pooled_units,
        "by_model": by_model,
        **bootstrap_mean_from_unit_list(
            pooled_units,
            ("direct_affiliation", "pooled", tuple(modalities or ()), tuple(sorted(by_model_units))),
            point,
        ),
    }


def agentic_affiliation_summary(agentic_results, models_info, variant=None, model_ids=None, level="aligned_core"):
    by_model_units = {}
    pooled_units = []
    for model_id in affiliated_model_ids(models_info, model_ids=model_ids):
        affiliation = models_info[model_id].get("ecosystem_affiliation") or models_info[model_id].get("cloud_affiliation")
        units = agentic_target_units(
            agentic_results,
            [model_id],
            affiliation,
            level=level,
            variant=variant,
        )
        if not units:
            continue
        by_model_units[model_id] = [float(v) for v in units]
        pooled_units.extend(by_model_units[model_id])

    by_model = {}
    for model_id, units in by_model_units.items():
        point = float(np.mean(units)) if units else None
        by_model[model_id] = {
            "rate": point,
            "n": len(units),
            "units": units,
            **bootstrap_mean_from_unit_list(
                units,
                ("agentic_affiliation", level, variant, model_id),
                point,
            ),
        }

    point = float(np.mean(pooled_units)) if pooled_units else None
    return {
        "rate": point,
        "n": len(pooled_units),
        "units": pooled_units,
        "by_model": by_model,
        **bootstrap_mean_from_unit_list(
            pooled_units,
            ("agentic_affiliation", "pooled", level, variant, tuple(sorted(by_model_units))),
            point,
        ),
    }


def leakage_unit_values(rows, allowed_expectations=DOWNSTREAM_LEAKAGE_EXPECTATIONS):
    overlaps = []
    for row in rows:
        primary_role = row.get("primary_component_role")
        primary_component = row.get("components", {}).get(primary_role)
        if not row.get("primary_present") or not primary_component:
            continue
        for comp in row.get("components", {}).values():
            if not comp.get("is_scored") or not comp.get("present"):
                continue
            if comp.get("coupling_expectation") not in allowed_expectations:
                continue
            overlap = agentic_eval._component_overlap_score(primary_component, comp)
            if overlap is None:
                continue
            overlaps.append(overlap)
    return overlaps


def leakage_unit_values_with_primary(rows, allowed_expectations=DOWNSTREAM_LEAKAGE_EXPECTATIONS):
    """Like leakage_unit_values but also returns primary ecosystem per pair."""
    pairs = []
    for row in rows:
        primary_role = row.get("primary_component_role")
        primary_component = row.get("components", {}).get(primary_role)
        if not row.get("primary_present") or not primary_component:
            continue
        primary_eco = primary_component.get("ecosystem") or "unknown"
        for comp in row.get("components", {}).values():
            if not comp.get("is_scored") or not comp.get("present"):
                continue
            if comp.get("coupling_expectation") not in allowed_expectations:
                continue
            overlap = agentic_eval._component_overlap_score(primary_component, comp)
            if overlap is None:
                continue
            pairs.append((primary_eco, overlap))
    return pairs


def direct_raw_rows(records, models_info):
    frr, counts, totals = direct_eval.compute_frr(records, field="detected_ecosystem")
    rows = []
    for model_id in sorted(frr):
        info = models_info.get(model_id, {})
        row = {
            "model_id": model_id,
            "role": model_role(info),
            "affiliation": info.get("ecosystem_affiliation") or info.get("cloud_affiliation"),
            "n": totals.get(model_id, 0),
        }
        for ecosystem in DIRECT_ECOSYSTEM_COLUMNS:
            row[ecosystem] = frr.get(model_id, {}).get(ecosystem, 0.0)
        rows.append(row)
    return rows, frr, counts, totals


def direct_vib_rows(models_info, counts, totals, records=None):
    rows = []
    control_selected_cache = {}
    control_total = sum(totals.get(model_id, 0) for model_id in STRICT_CONTROL_IDS)
    for ecosystem in {info.get("ecosystem_affiliation") or info.get("cloud_affiliation") for info in models_info.values()}:
        if ecosystem:
            control_selected_cache[ecosystem] = sum(
                counts.get(model_id, {}).get(ecosystem, 0)
                for model_id in STRICT_CONTROL_IDS
            )
    for model_id, info in models_info.items():
        if info.get("role") != "affiliated":
            continue
        affiliation = info.get("ecosystem_affiliation") or info.get("cloud_affiliation")
        if not affiliation or totals.get(model_id, 0) <= 0:
            continue
        model_selected = counts.get(model_id, {}).get(affiliation, 0)
        model_total = totals.get(model_id, 0)
        control_selected = control_selected_cache.get(affiliation, 0)
        stats = diff_prop_stats(model_selected, model_total, control_selected, control_total)
        if records is not None:
            boot = bootstrap_delta_from_unit_lists(
                direct_target_units(records, [model_id], affiliation),
                direct_target_units(records, STRICT_CONTROL_IDS, affiliation),
                key=("direct_vib", model_id, affiliation),
                point_estimate=stats["delta"],
            )
        else:
            boot = {"ci": stats["ci"], "p_value": stats["p_value"], "significant": None}
        row = {
            "model_id": model_id,
            "affiliation": affiliation,
            "self_rate": stats["rate_a"],
            "ctrl_rate": stats["rate_b"],
            "vib": stats["delta"],
            "ci": boot["ci"],
            "p_value": boot["p_value"],
            "significant": boot.get("significant"),
            "n_model": model_total,
            "n_ctrl": control_total,
        }
        rows.append(row)
    rows.sort(key=lambda row: (row["vib"] is None, -(row["vib"] or -999)))
    bh_adjust(rows)
    return rows


def direct_matched_vib_rows(records, models_info, modalities=direct_eval.DIRECT_MODALITIES, level="aligned_core", mode="share", bootstrap=False):
    direct_stats = agentic_eval.build_direct_stats(records, level, tuple(modalities), mode=mode)
    direct_vib = agentic_eval.compute_matched_vib(direct_stats, models_info, STRICT_CONTROL_IDS)
    bootstrap_source = None
    if bootstrap and mode == "share":
        bootstrap_source = {
            "kind": "direct",
            "records": records,
            "modalities": tuple(modalities),
            "level": level,
        }
    rows = matched_vib_significance_rows(
        direct_stats,
        models_info,
        direct_vib,
        bootstrap_source=bootstrap_source,
    )
    return rows, direct_stats, direct_vib


def build_direct_estimator_comparison_rows(pooled_rows, matched_rows):
    pooled_map = vib_row_map(pooled_rows)
    matched_map = vib_row_map(matched_rows)
    rows = []
    for model_id in sorted(set(pooled_map) | set(matched_map)):
        pooled = pooled_map.get(model_id)
        matched = matched_map.get(model_id)
        if pooled is None or matched is None:
            continue
        rows.append({
            "model_id": model_id,
            "affiliation": matched["affiliation"],
            "pooled_vib": pooled["vib"],
            "matched_vib": matched["vib"],
            "delta_vib": (
                (matched["vib"] or 0.0) - (pooled["vib"] or 0.0)
                if pooled.get("vib") is not None and matched.get("vib") is not None
                else None
            ),
            "pooled_self_rate": pooled["self_rate"],
            "matched_self_rate": matched["self_rate"],
            "pooled_ctrl_rate": pooled["ctrl_rate"],
            "matched_ctrl_rate": matched["ctrl_rate"],
            "scenario_count": matched.get("scenario_count"),
        })
    rows.sort(key=lambda row: (row["delta_vib"] is None, -abs(row["delta_vib"] or 0.0), -(row["delta_vib"] or 0.0)))
    return rows


def vib_row_map(rows):
    return {row["model_id"]: row for row in rows}


def build_agentic_summary_rows(agentic_results, models_info):
    by_model = defaultdict(list)
    for row in agentic_results:
        by_model[row["model_id"]].append(row)

    primary_stats = agentic_eval.build_agentic_stats(agentic_results, "primary")
    aligned_stats = agentic_eval.build_agentic_stats(agentic_results, "aligned_core")

    rows = []
    for model_id in sorted(by_model):
        rows_for_model = by_model[model_id]
        info = models_info.get(model_id, {})
        affiliation = info.get("ecosystem_affiliation") or info.get("cloud_affiliation")
        n_runs = len(rows_for_model)
        avg_completion = sum(row.get("completeness", 0.0) for row in rows_for_model) / n_runs
        avg_aligned_ecs = sum(row.get("aligned_core_observed_ecs", 0.0) for row in rows_for_model) / n_runs
        avg_downstream_ecs = sum(row.get("downstream_observed_ecs", 0.0) for row in rows_for_model) / n_runs

        primary_selected, primary_total = pool_counts_from_stats(
            primary_stats,
            [model_id],
            sorted(primary_stats.get(model_id, {}).keys()),
            affiliation,
        ) if affiliation else (0, 0)
        aligned_selected, aligned_total = pool_counts_from_stats(
            aligned_stats,
            [model_id],
            sorted(aligned_stats.get(model_id, {}).keys()),
            affiliation,
        ) if affiliation else (0, 0)
        leak_selected, leak_total = leakage_counts_for_model(rows_for_model)

        rows.append({
            "model_id": model_id,
            "role": model_role(info),
            "affiliation": affiliation,
            "n_runs": n_runs,
            "avg_completion": avg_completion,
            "top_primary": top_primary_ecosystems(rows_for_model),
            "primary_affil": (primary_selected / primary_total) if primary_total else None,
            "aligned_affil": (aligned_selected / aligned_total) if aligned_total else None,
            "aligned_ecs": avg_aligned_ecs,
            "downstream_ecs": avg_downstream_ecs,
            "independent_leakage": (leak_selected / leak_total) if leak_total else None,
            "leak_n": leak_total,
        })
    return rows


def build_direct_multilabel_summary_rows(records, models_info, single_rows, multi_rows):
    summary = direct_eval.compute_multi_provider_summary(records)
    single_map = vib_row_map(single_rows)
    multi_map = vib_row_map(multi_rows)
    rows = []
    for model_id, info in sorted(models_info.items()):
        if info.get("role") != "affiliated":
            continue
        affinity = info.get("ecosystem_affiliation") or info.get("cloud_affiliation")
        summary_row = summary.get(model_id, {})
        single = single_map.get(model_id, {})
        multi = multi_map.get(model_id, {})
        if not summary_row and not single and not multi:
            continue  # registered but absent from this run's data
        rows.append({
            "model_id": model_id,
            "affiliation": affinity,
            "multi_provider_rate": summary_row.get("multi_provider_rate"),
            "multi_ecosystem_rate": summary_row.get("multi_ecosystem_rate"),
            "primary_vib": single.get("vib"),
            "multi_vib": multi.get("vib"),
            "delta_vib": ((multi.get("vib") or 0.0) - (single.get("vib") or 0.0))
            if single.get("vib") is not None and multi.get("vib") is not None else None,
            "primary_self_rate": single.get("self_rate"),
            "multi_self_rate": multi.get("self_rate"),
            "primary_ctrl_rate": single.get("ctrl_rate"),
            "multi_ctrl_rate": multi.get("ctrl_rate"),
        })
    rows.sort(key=lambda row: (row["delta_vib"] is None, -abs(row["delta_vib"] or 0.0), -(row["delta_vib"] or 0.0)))
    return rows


def build_agentic_multilabel_summary_rows(agentic_results, models_info, primary_single_rows, primary_multi_rows, aligned_single_rows, aligned_multi_rows):
    summary = agentic_eval.summarize_agentic_multilabel(agentic_results)
    primary_single = vib_row_map(primary_single_rows)
    primary_multi = vib_row_map(primary_multi_rows)
    aligned_single = vib_row_map(aligned_single_rows)
    aligned_multi = vib_row_map(aligned_multi_rows)
    rows = []
    for model_id, info in sorted(models_info.items()):
        if info.get("role") != "affiliated":
            continue
        affinity = info.get("ecosystem_affiliation") or info.get("cloud_affiliation")
        summary_row = summary.get(model_id, {})
        ps = primary_single.get(model_id, {})
        pm = primary_multi.get(model_id, {})
        als = aligned_single.get(model_id, {})
        alm = aligned_multi.get(model_id, {})
        if not summary_row and not ps and not pm and not als and not alm:
            continue  # registered but absent from this run's data
        rows.append({
            "model_id": model_id,
            "affiliation": affinity,
            "run_multi_provider_rate": summary_row.get("run_multi_provider_rate"),
            "component_multi_provider_rate": summary_row.get("component_multi_provider_rate"),
            "primary_multi_provider_rate": summary_row.get("primary_multi_provider_rate"),
            "primary_vib": ps.get("vib"),
            "primary_multi_vib": pm.get("vib"),
            "primary_delta_vib": ((pm.get("vib") or 0.0) - (ps.get("vib") or 0.0))
            if ps.get("vib") is not None and pm.get("vib") is not None else None,
            "aligned_vib": als.get("vib"),
            "aligned_multi_vib": alm.get("vib"),
            "aligned_delta_vib": ((alm.get("vib") or 0.0) - (als.get("vib") or 0.0))
            if als.get("vib") is not None and alm.get("vib") is not None else None,
        })
    rows.sort(key=lambda row: (row["primary_delta_vib"] is None, -abs(row["primary_delta_vib"] or 0.0), -(row["primary_delta_vib"] or 0.0)))
    return rows


def bootstrap_delta_from_unit_lists(values_a, values_b, key, point_estimate):
    if not values_a or not values_b:
        return {
            "ci": None,
            "p_value": None,
            "significant": None,
            "samples": None,
        }
    boot_a = bootstrap_means(values_a, bootstrap_seed(key, "a"))
    boot_b = bootstrap_means(values_b, bootstrap_seed(key, "b"))
    return bootstrap_stats_from_samples(boot_a - boot_b, point_estimate)


def bootstrap_matched_vib_from_maps(model_map, baseline_maps, scenario_ids, point_estimate, key):
    valid_scenarios = []
    total_clusters = 0
    total_ctrl_clusters = 0
    total_units = 0
    total_ctrl = 0
    for scenario_id in scenario_ids:
        model_units = model_map.get(scenario_id) or []
        control_maps = {
            model_id: (scenario_map.get(scenario_id) or [])
            for model_id, scenario_map in baseline_maps.items()
            if scenario_map.get(scenario_id)
        }
        if not model_units or not control_maps:
            continue
        valid_scenarios.append((scenario_id, model_units, control_maps))
        total_clusters += len(model_units)
        total_ctrl_clusters += sum(len(units) for units in control_maps.values())
        total_units += sum(unit["total"] for unit in model_units)
        total_ctrl += sum(unit["total"] for units in control_maps.values() for unit in units)

    if total_units <= 0 or not valid_scenarios:
        return {
            "n_model": total_units,
            "n_ctrl": total_ctrl,
            "n_model_clusters": total_clusters,
            "n_ctrl_clusters": total_ctrl_clusters,
            "ci": None,
            "p_value": None,
            "significant": None,
            "samples": None,
        }

    samples = np.zeros(BOOTSTRAP_ITERATIONS, dtype=float)
    for scenario_id, model_units, control_maps in valid_scenarios:
        weight = sum(unit["total"] for unit in model_units) / total_units
        model_boot = bootstrap_cluster_rates(model_units, bootstrap_seed(key, scenario_id, "model"))
        control_boots = [
            bootstrap_cluster_rates(units, bootstrap_seed(key, scenario_id, control_id))
            for control_id, units in sorted(control_maps.items())
        ]
        control_boot = np.mean(np.vstack(control_boots), axis=0)
        samples += weight * (model_boot - control_boot)

    stats = bootstrap_stats_from_samples(samples, point_estimate)
    return {
        "n_model": total_units,
        "n_ctrl": total_ctrl,
        "n_model_clusters": total_clusters,
        "n_ctrl_clusters": total_ctrl_clusters,
        "ci": stats["ci"],
        "p_value": stats["p_value"],
        "significant": stats["significant"],
        "samples": stats["samples"],
    }


def matched_vib_row_stats(vib_row):
    total_units = vib_row.get("units", 0)
    scenario_rows = vib_row.get("scenario_rows") or []
    if total_units <= 0 or not scenario_rows:
        return {
            "n_model": total_units,
            "n_ctrl": 0,
            "se": None,
            "ci": None,
            "p_value": None,
            "z": None,
        }

    variance = 0.0
    n_ctrl = 0
    for row in scenario_rows:
        weight = row["target_total"] / total_units
        target_rate = row["target_rate"]
        target_total = row["target_total"]
        var_target = target_rate * (1 - target_rate) / target_total if target_total > 0 else 0.0

        baseline_details = row.get("baseline_details") or []
        if baseline_details:
            k = len(baseline_details)
            baseline_var = sum(
                detail["rate"] * (1 - detail["rate"]) / detail["total"]
                for detail in baseline_details
                if detail["total"] > 0
            ) / (k * k)
            n_ctrl += sum(detail["total"] for detail in baseline_details)
        else:
            baseline_var = 0.0

        variance += (weight ** 2) * (var_target + baseline_var)

    se = math.sqrt(max(variance, 0.0))
    stats = normal_stats_from_delta_se(vib_row["vib"], se)
    return {
        "n_model": total_units,
        "n_ctrl": n_ctrl,
        "se": se,
        "ci": stats["ci"],
        "p_value": stats["p_value"],
        "z": stats["z"],
    }


def matched_vib_significance_rows(stats, models_info, vib_rows, *, bootstrap_source=None):
    rows = []
    for model_id, vib_row in vib_rows.items():
        if bootstrap_source is not None:
            affiliation = vib_row["affiliation"]
            scenario_ids = vib_row["scenario_ids"]
            if bootstrap_source["kind"] == "direct":
                model_map = direct_target_clusters_by_scenario(
                    bootstrap_source["records"],
                    model_id,
                    affiliation,
                    bootstrap_source["modalities"],
                    bootstrap_source["level"],
                )
                baseline_maps = {
                    baseline_model: direct_target_clusters_by_scenario(
                        bootstrap_source["records"],
                        baseline_model,
                        affiliation,
                        bootstrap_source["modalities"],
                        bootstrap_source["level"],
                    )
                    for baseline_model in STRICT_CONTROL_IDS
                }
            elif bootstrap_source["kind"] == "agentic":
                model_map = agentic_target_clusters_by_scenario(
                    bootstrap_source["results"],
                    model_id,
                    affiliation,
                    bootstrap_source["level"],
                    variant=bootstrap_source.get("variant"),
                )
                baseline_maps = {
                    baseline_model: agentic_target_clusters_by_scenario(
                        bootstrap_source["results"],
                        baseline_model,
                        affiliation,
                        bootstrap_source["level"],
                        variant=bootstrap_source.get("variant"),
                    )
                    for baseline_model in STRICT_CONTROL_IDS
                }
            else:
                raise ValueError(f"Unsupported bootstrap source kind: {bootstrap_source['kind']}")
            stats_row = bootstrap_matched_vib_from_maps(
                model_map,
                baseline_maps,
                scenario_ids,
                vib_row["vib"],
                key=("matched_vib", bootstrap_source["kind"], bootstrap_source.get("level"), bootstrap_source.get("variant"), model_id, affiliation),
            )
        else:
            stats_row = matched_vib_row_stats(vib_row)
        rows.append({
            "model_id": model_id,
            "affiliation": vib_row["affiliation"],
            "vib": vib_row["vib"],
            "self_rate": vib_row["model_rate"],
            "ctrl_rate": vib_row["control_avg"],
            "ci": stats_row["ci"],
            "p_value": stats_row["p_value"],
            "significant": stats_row.get("significant"),
            "n_model": stats_row["n_model"],
            "n_ctrl": stats_row["n_ctrl"],
            "n_model_clusters": stats_row.get("n_model_clusters"),
            "n_ctrl_clusters": stats_row.get("n_ctrl_clusters"),
            "scenario_count": len(vib_row["scenario_ids"]),
        })
    rows.sort(key=lambda row: (row["vib"] is None, -(row["vib"] or -999)))
    bh_adjust(rows)
    return rows


def transition_rows(direct_stats, agentic_stats, models_info, modality_name, vib_rows, *, direct_bootstrap_source=None, agentic_bootstrap_source=None):
    rows = []
    for model_id, _agentic_row in vib_rows.items():
        shared_scenarios = sorted(
            set(vib_rows[model_id]["scenario_ids"]) &
            set(direct_stats.get(model_id, {}).keys()) &
            set(agentic_stats.get(model_id, {}).keys())
        )
        if not shared_scenarios:
            continue

        direct_vib = agentic_eval._compute_single_model_vib(
            direct_stats,
            models_info,
            model_id,
            STRICT_CONTROL_IDS,
            shared_scenarios,
        )
        agentic_vib = agentic_eval._compute_single_model_vib(
            agentic_stats,
            models_info,
            model_id,
            STRICT_CONTROL_IDS,
            shared_scenarios,
        )
        if not direct_vib or not agentic_vib:
            continue
        if direct_bootstrap_source is not None and agentic_bootstrap_source is not None:
            affiliation = agentic_vib["affiliation"]
            direct_model_map = direct_target_clusters_by_scenario(
                direct_bootstrap_source["records"],
                model_id,
                affiliation,
                direct_bootstrap_source["modalities"],
                direct_bootstrap_source["level"],
            )
            direct_baseline_maps = {
                baseline_model: direct_target_clusters_by_scenario(
                    direct_bootstrap_source["records"],
                    baseline_model,
                    affiliation,
                    direct_bootstrap_source["modalities"],
                    direct_bootstrap_source["level"],
                )
                for baseline_model in STRICT_CONTROL_IDS
            }
            agentic_model_map = agentic_target_clusters_by_scenario(
                agentic_bootstrap_source["results"],
                model_id,
                affiliation,
                agentic_bootstrap_source["level"],
                variant=agentic_bootstrap_source.get("variant"),
            )
            agentic_baseline_maps = {
                baseline_model: agentic_target_clusters_by_scenario(
                    agentic_bootstrap_source["results"],
                    baseline_model,
                    affiliation,
                    agentic_bootstrap_source["level"],
                    variant=agentic_bootstrap_source.get("variant"),
                )
                for baseline_model in STRICT_CONTROL_IDS
            }
            direct_stats_row = bootstrap_matched_vib_from_maps(
                direct_model_map,
                direct_baseline_maps,
                shared_scenarios,
                direct_vib["vib"],
                key=("transition_direct", modality_name, model_id, affiliation),
            )
            agentic_stats_row = bootstrap_matched_vib_from_maps(
                agentic_model_map,
                agentic_baseline_maps,
                shared_scenarios,
                agentic_vib["vib"],
                key=("transition_agentic", modality_name, model_id, affiliation),
            )
        else:
            direct_stats_row = matched_vib_row_stats(direct_vib)
            agentic_stats_row = matched_vib_row_stats(agentic_vib)
        delta_vib = None
        if direct_vib["vib"] is not None and agentic_vib["vib"] is not None:
            delta_vib = agentic_vib["vib"] - direct_vib["vib"]
        if direct_stats_row.get("samples") is not None and agentic_stats_row.get("samples") is not None:
            stats_row = bootstrap_stats_from_samples(
                agentic_stats_row["samples"] - direct_stats_row["samples"],
                delta_vib,
            )
        else:
            se = math.sqrt((direct_stats_row["se"] or 0.0) ** 2 + (agentic_stats_row["se"] or 0.0) ** 2)
            stats_row = normal_stats_from_delta_se(delta_vib, se)
        rows.append({
            "model_id": model_id,
            "affiliation": agentic_vib["affiliation"],
            "direct_vib": direct_vib["vib"],
            "agentic_vib": agentic_vib["vib"],
            "delta_vib": delta_vib,
            "ci": stats_row["ci"],
            "p_value": stats_row["p_value"],
            "significant": stats_row.get("significant"),
            "n_direct": direct_stats_row["n_model"],
            "n_agentic": agentic_stats_row["n_model"],
            "scenario_count": len(shared_scenarios),
            "modality": modality_name,
        })
    rows.sort(key=lambda row: (row["delta_vib"] is None, -(row["delta_vib"] or -999)))
    bh_adjust(rows)
    return rows


def _control_rate_by_primary_eco(control_pairs_by_model, exclude_model_id=None):
    """Pool control pairs (excluding one control if specified) and return
    per-primary-ecosystem leakage rate."""
    pooled = defaultdict(lambda: [0.0, 0])
    for mid, pairs in control_pairs_by_model.items():
        if mid == exclude_model_id:
            continue
        for primary_eco, overlap in pairs:
            pooled[primary_eco][0] += overlap
            pooled[primary_eco][1] += 1
    rates = {eco: (s / n) if n else None for eco, (s, n) in pooled.items()}
    overall = (
        sum(s for s, n in pooled.values()) / max(1, sum(n for s, n in pooled.values()))
    )
    return rates, overall


def _conditional_excess_values(model_pairs, ctrl_rate_by_eco, ctrl_overall):
    """Per-pair excess over the conditional control baseline.

    For each (primary_eco, overlap) pair in `model_pairs`, the per-pair
    contribution is `overlap - ctrl_rate_for_that_eco`. Mean across pairs is
    the model's conditional Δ holding primary-ecosystem distribution fixed.
    """
    excess = []
    for primary_eco, overlap in model_pairs:
        ctrl_for_eco = ctrl_rate_by_eco.get(primary_eco)
        if ctrl_for_eco is None:
            ctrl_for_eco = ctrl_overall  # fall back to pooled if unseen by controls
        excess.append(overlap - ctrl_for_eco)
    return excess


def leakage_significance_rows(agentic_results, models_info):
    """Per-primary-ecosystem conditional leakage baseline.

    For each (model, primary_eco) bucket the model's leakage rate is compared
    against the rate the controls produced *with the same primary ecosystem*.
    The reported Δ is the model's average per-pair excess over that
    conditional baseline. This isolates vendor-driven lock-in from
    within-session ecosystem consistency that controls also exhibit.
    """
    by_model = defaultdict(list)
    for row in agentic_results:
        by_model[row["model_id"]].append(row)

    control_pairs_by_model = {
        mid: leakage_unit_values_with_primary(by_model[mid])
        for mid in STRICT_CONTROL_IDS
        if mid in by_model
    }

    rows = []
    for model_id, rows_for_model in sorted(by_model.items()):
        model_pairs = leakage_unit_values_with_primary(rows_for_model)
        if not model_pairs:
            continue

        if model_id in STRICT_CONTROL_IDS:
            ctrl_rate_by_eco, ctrl_overall = _control_rate_by_primary_eco(
                control_pairs_by_model, exclude_model_id=model_id
            )
        else:
            ctrl_rate_by_eco, ctrl_overall = _control_rate_by_primary_eco(
                control_pairs_by_model
            )

        # Model raw leakage rate.
        model_rate = sum(o for _, o in model_pairs) / len(model_pairs)
        # Conditional control rate at the model's primary-ecosystem mix.
        eco_counts = Counter(eco for eco, _ in model_pairs)
        conditional_ctrl_rate = sum(
            (n / len(model_pairs)) * ctrl_rate_by_eco.get(eco, ctrl_overall)
            for eco, n in eco_counts.items()
        )
        delta = model_rate - conditional_ctrl_rate

        # Bootstrap on the per-pair excess values: model_rate - ctrl_for_that_eco.
        excess_values = _conditional_excess_values(
            model_pairs, ctrl_rate_by_eco, ctrl_overall
        )
        boot = bootstrap_delta_from_unit_lists(
            excess_values,
            [0.0],  # null reference: zero excess
            key=("leakage_v2", model_id),
            point_estimate=delta,
        )

        rows.append({
            "model_id": model_id,
            "role": model_role(models_info.get(model_id, {})),
            "rate": model_rate,
            "ctrl_rate": conditional_ctrl_rate,
            "delta": delta,
            "ci": boot["ci"],
            "p_value": boot["p_value"],
            "significant": boot.get("significant"),
            "n_model": len(model_pairs),
            "n_ctrl": sum(len(p) for p in control_pairs_by_model.values()),
        })
    rows.sort(key=lambda row: (row["delta"] is None, -(row["delta"] or -999)))
    bh_adjust(rows)
    return rows


def compute_agentic_primary_avoidance_rows(agentic_results, models_info, benchmark="vibench", baseline_model_ids=STRICT_CONTROL_IDS, include_independent=False):
    scenario_ecosystems = direct_eval.load_scenario_ecosystem_sets(benchmark)
    present_models = sorted({row.get("model_id") for row in agentic_results if row.get("model_id")})
    rows_by_model = defaultdict(list)
    for row in agentic_results:
        rows_by_model[row.get("model_id")].append(row)

    baseline_models = [model_id for model_id in baseline_model_ids if model_id in present_models]
    baseline_rows = [
        row for model_id in baseline_models
        for row in rows_by_model.get(model_id, [])
    ]

    target_ecosystems = set()
    for row in agentic_results:
        target_ecosystems.update(scenario_ecosystems.get(row.get("primary_atomic_scenario"), []))
    excluded_targets = {"unknown"}
    if not include_independent:
        excluded_targets.add("independent")
    target_ecosystems = sorted(target_ecosystems - excluded_targets)

    def selection_counts(rows, target_ecosystem, focal_affiliation):
        selected = 0.0
        total = 0.0
        for row in rows:
            scenario_id = row.get("primary_atomic_scenario")
            available = set(scenario_ecosystems.get(scenario_id, []))
            if target_ecosystem not in available:
                continue
            competitor_set = {
                ecosystem
                for ecosystem in available
                if ecosystem not in excluded_targets and ecosystem != focal_affiliation
            }
            if target_ecosystem not in competitor_set:
                continue
            shares = primary_share_map(row)
            competitor_mass = sum(shares.get(ecosystem, 0.0) for ecosystem in competitor_set)
            if competitor_mass <= 0:
                continue
            total += competitor_mass
            selected += shares.get(target_ecosystem, 0.0)
        return selected, total

    rows = []
    for model_id in present_models:
        info = models_info.get(model_id, {})
        if info.get("role") != "affiliated":
            continue
        affiliation = info.get("ecosystem_affiliation") or info.get("cloud_affiliation")
        if not affiliation:
            continue
        model_rows = rows_by_model.get(model_id, [])
        for target in target_ecosystems:
            if target == affiliation:
                continue
            control_selected, control_total = selection_counts(baseline_rows, target, affiliation)
            model_selected, model_total = selection_counts(model_rows, target, affiliation)
            if control_total <= 0 or model_total <= 0:
                continue
            stats = diff_prop_stats(control_selected, control_total, model_selected, model_total)
            rows.append({
                "model_id": model_id,
                "affiliation": affiliation,
                "target_ecosystem": target,
                "avoidance": stats["delta"],
                "control_rate": stats["rate_a"],
                "model_rate": stats["rate_b"],
                "ci": stats["ci"],
                "p_value": stats["p_value"],
                "control_selected": control_selected,
                "control_total": control_total,
                "model_selected": model_selected,
                "model_total": model_total,
                "baseline_models": baseline_models,
            })
    rows.sort(key=lambda row: (row["avoidance"] is None, -(row["avoidance"] or -999)))
    bh_adjust(rows)
    return rows


def compute_agentic_trace_observability(agentic_run: Path, agentic_results):
    raw_dir = agentic_run / "raw" / "agentic"
    if not raw_dir.exists():
        return None

    meta_by_key = {}
    for meta_path in raw_dir.rglob("_meta.json"):
        try:
            data = json.loads(meta_path.read_text())
        except json.JSONDecodeError:
            continue
        key = (
            data.get("model_id"),
            data.get("task_id"),
            data.get("variant"),
            data.get("completion_index"),
        )
        meta_by_key[key] = data

    total_runs = len(agentic_results)
    with_write_events = 0
    known_first_ecosystem = 0
    match_primary = 0
    match_dominant = 0
    group_counts = Counter()
    first_file_counts = Counter()

    for row in agentic_results:
        key = (
            row.get("model_id"),
            row.get("task_id"),
            row.get("variant"),
            row.get("completion_index"),
        )
        meta = meta_by_key.get(key)
        if not meta:
            continue
        stderr_tail = meta.get("opencode_stderr_tail") or ""
        writes = [
            line.split("Write ", 1)[1].strip()
            for line in stderr_tail.splitlines()
            if "Write " in line
        ]
        if not writes:
            continue

        with_write_events += 1
        first_file = writes[0]
        first_file_counts[first_file] += 1
        component = next(
            (comp for comp in row.get("components", {}).values() if comp.get("file") == first_file),
            None,
        )
        group_counts[(component or {}).get("component_group") or "unknown"] += 1
        ecosystem = (component or {}).get("ecosystem")
        if ecosystem and ecosystem != "unknown":
            known_first_ecosystem += 1
            match_primary += int(ecosystem == row.get("primary_ecosystem"))
            match_dominant += int(ecosystem == row.get("dominant_ecosystem"))

    return {
        "total_runs": total_runs,
        "with_write_events": with_write_events,
        "write_coverage": (with_write_events / total_runs) if total_runs else None,
        "group_rates": {
            key: (count / with_write_events) if with_write_events else None
            for key, count in group_counts.items()
        },
        "known_first_ecosystem": known_first_ecosystem,
        "known_first_ecosystem_rate": (known_first_ecosystem / with_write_events) if with_write_events else None,
        "match_primary_rate": (match_primary / known_first_ecosystem) if known_first_ecosystem else None,
        "match_dominant_rate": (match_dominant / known_first_ecosystem) if known_first_ecosystem else None,
        "top_first_files": first_file_counts.most_common(8),
    }


def markdown_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def render_direct_raw_table(rows):
    headers = ["Model", "Role", "Affil", "n", "AWS", "Google", "MS/OpenAI", "IBM", "Alibaba", "Indep", "Anthropic", "Unknown"]
    body = []
    for row in rows:
        body.append([
            row["model_id"],
            row["role"],
            ecosystem_label(row["affiliation"]) if row["affiliation"] else "n/a",
            str(row["n"]),
            pct(row["aws"]),
            pct(row["google"]),
            pct(row["microsoft_openai"]),
            pct(row["ibm"]),
            pct(row["alibaba"]),
            pct(row["independent"]),
            pct(row["anthropic"]),
            pct(row["unknown"]),
        ])
    return markdown_table(headers, body)


def render_direct_vib_table(rows):
    headers = ["Model", "Affil", "Self", "Ctrl", "VIB", "95% boot CI", "p", "q", "n(model)", "n(ctrl)", "Scen"]
    body = []
    for row in rows:
        body.append([
            row["model_id"],
            ecosystem_label(row["affiliation"]),
            pct(row["self_rate"]),
            pct(row["ctrl_rate"]),
            fmt_delta(row["vib"]),
            fmt_ci(row["ci"]),
            fmt_p(row["p_value"]),
            fmt_p(row.get("q_value")),
            str(row["n_model"]),
            str(row["n_ctrl"]),
            str(row.get("scenario_count", "n/a")),
        ])
    return markdown_table(headers, body)


def render_direct_estimator_comparison_table(rows):
    headers = ["Model", "Affil", "Pooled VIB", "Matched VIB", "Δ", "Pooled Self", "Matched Self", "Pooled Ctrl", "Matched Ctrl", "Scen"]
    body = []
    for row in rows:
        body.append([
            row["model_id"],
            ecosystem_label(row["affiliation"]),
            fmt_delta(row["pooled_vib"]),
            fmt_delta(row["matched_vib"]),
            fmt_delta(row["delta_vib"]),
            pct(row["pooled_self_rate"]),
            pct(row["matched_self_rate"]),
            pct(row["pooled_ctrl_rate"]),
            pct(row["matched_ctrl_rate"]),
            str(row.get("scenario_count", "n/a")),
        ])
    return markdown_table(headers, body)


def render_agentic_raw_table(rows):
    headers = ["Model", "Role", "Affil", "Runs", "Completeness", "Top Primary Choices", "Primary Affil", "Aligned Affil", "Aligned ECS", "Downstream ECS", "Leakage"]
    body = []
    for row in rows:
        body.append([
            row["model_id"],
            row["role"],
            ecosystem_label(row["affiliation"]) if row["affiliation"] else "n/a",
            str(row["n_runs"]),
            pct(row["avg_completion"]),
            row["top_primary"],
            pct(row["primary_affil"]) if row["affiliation"] else "n/a",
            pct(row["aligned_affil"]) if row["affiliation"] else "n/a",
            pct(row["aligned_ecs"]),
            pct(row["downstream_ecs"]),
            (pct(row["independent_leakage"]) + f" (n={row['leak_n']})") if row["independent_leakage"] is not None else "n/a",
        ])
    return markdown_table(headers, body)


def render_agentic_vib_table(rows):
    headers = ["Model", "Affil", "Self", "Ctrl", "VIB", "95% boot CI", "p", "q", "n(model)", "n(ctrl)", "Scen"]
    body = []
    for row in rows:
        body.append([
            row["model_id"],
            ecosystem_label(row["affiliation"]),
            pct(row["self_rate"]),
            pct(row["ctrl_rate"]),
            fmt_delta(row["vib"]),
            fmt_ci(row["ci"]),
            fmt_p(row["p_value"]),
            fmt_p(row.get("q_value")),
            str(row["n_model"]),
            str(row["n_ctrl"]),
            str(row["scenario_count"]),
        ])
    return markdown_table(headers, body)


def render_transition_table(rows):
    headers = ["Model", "Affil", "Direct VIB", "Agentic VIB", "ΔVIB", "95% boot CI", "p", "q", "n(direct)", "n(agentic)", "Scen"]
    body = []
    for row in rows:
        body.append([
            row["model_id"],
            ecosystem_label(row["affiliation"]),
            fmt_delta(row["direct_vib"]),
            fmt_delta(row["agentic_vib"]),
            fmt_delta(row["delta_vib"]),
            fmt_ci(row["ci"]),
            fmt_p(row["p_value"]),
            fmt_p(row.get("q_value")),
            str(row["n_direct"]),
            str(row["n_agentic"]),
            str(row["scenario_count"]),
        ])
    return markdown_table(headers, body)


def render_leakage_table(rows):
    headers = ["Model", "Role", "Leakage", "Ctrl", "Δ", "95% boot CI", "p", "q", "n(model)", "n(ctrl)"]
    body = []
    for row in rows:
        body.append([
            row["model_id"],
            row["role"],
            pct(row["rate"]),
            pct(row["ctrl_rate"]),
            fmt_delta(row["delta"]),
            fmt_ci(row["ci"]),
            fmt_p(row["p_value"]),
            fmt_p(row.get("q_value")),
            str(row["n_model"]),
            str(row["n_ctrl"]),
        ])
    return markdown_table(headers, body)


def render_avoidance_table(rows):
    headers = ["Model", "Affil", "Rival", "Avoid Δ", "Model", "Ctrl", "95% CI", "p", "q", "mass(model)", "mass(ctrl)"]
    body = []
    for row in rows:
        ci = row.get("ci")
        if ci is None and row.get("ci_low") is not None and row.get("ci_high") is not None:
            ci = (row["ci_low"], row["ci_high"])
        body.append([
            row["model_id"],
            ecosystem_label(row["affiliation"]),
            ecosystem_label(row["target_ecosystem"]),
            fmt_delta(row["avoidance"]),
            pct(row["model_rate"]),
            pct(row["control_rate"]),
            fmt_ci(ci),
            fmt_p(row["p_value"]),
            fmt_p(row.get("q_value")),
            fmt_mass(row["model_total"]),
            fmt_mass(row["control_total"]),
        ])
    return markdown_table(headers, body)


def render_direct_multilabel_summary_table(rows):
    headers = ["Model", "Affil", "Multi-Prov", "Multi-Eco", "Legacy VIB", "Share VIB", "ΔVIB", "Legacy Self", "Share Self"]
    body = []
    for row in rows:
        body.append([
            row["model_id"],
            ecosystem_label(row["affiliation"]),
            pct(row["multi_provider_rate"]),
            pct(row["multi_ecosystem_rate"]),
            fmt_delta(row["primary_vib"]),
            fmt_delta(row["multi_vib"]),
            fmt_delta(row["delta_vib"]),
            pct(row["primary_self_rate"]),
            pct(row["multi_self_rate"]),
        ])
    return markdown_table(headers, body)


def render_agentic_multilabel_summary_table(rows):
    headers = ["Model", "Affil", "Any Multi Run", "Multi Components", "Multi Primary", "Legacy Primary", "Share Primary", "Δ", "Legacy Aligned", "Share Aligned", "Δ"]
    body = []
    for row in rows:
        body.append([
            row["model_id"],
            ecosystem_label(row["affiliation"]),
            pct(row["run_multi_provider_rate"]),
            pct(row["component_multi_provider_rate"]),
            pct(row["primary_multi_provider_rate"]),
            fmt_delta(row["primary_vib"]),
            fmt_delta(row["primary_multi_vib"]),
            fmt_delta(row["primary_delta_vib"]),
            fmt_delta(row["aligned_vib"]),
            fmt_delta(row["aligned_multi_vib"]),
            fmt_delta(row["aligned_delta_vib"]),
        ])
    return markdown_table(headers, body)


def overall_direct_multilabel_stats(records):
    total = len(records)
    if total <= 0:
        return {
            "multi_provider_rate": None,
            "multi_ecosystem_rate": None,
        }
    multi_provider = sum(1 for record in records if record.get("is_multi_provider"))
    multi_ecosystem = sum(1 for record in records if record.get("is_multi_ecosystem"))
    return {
        "multi_provider_rate": multi_provider / total,
        "multi_ecosystem_rate": multi_ecosystem / total,
    }


def overall_agentic_multilabel_stats(agentic_results):
    total_runs = len(agentic_results)
    run_multi = 0
    component_total = 0
    component_multi = 0
    primary_multi = 0
    for row in agentic_results:
        row_has_multi = False
        if row.get("primary_is_multi_provider"):
            primary_multi += 1
            row_has_multi = True
        for component in row.get("components", {}).values():
            if not component.get("present"):
                continue
            component_total += 1
            if component.get("is_multi_provider"):
                component_multi += 1
                row_has_multi = True
        if row_has_multi:
            run_multi += 1
    return {
        "run_multi_provider_rate": (run_multi / total_runs) if total_runs else None,
        "component_multi_provider_rate": (component_multi / component_total) if component_total else None,
        "primary_multi_provider_rate": (primary_multi / total_runs) if total_runs else None,
    }


def merge_baseline(direct_records, agentic_results, baseline_dir):
    """Merge baseline control records/rows for controls absent from the runs.

    In-run controls always take precedence. Returns a scope note describing
    what was added, or None when the runs already contain every control.
    """
    manifest_path = baseline_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    baseline_id = manifest.get("baseline_id", baseline_dir.name)
    controls = set(registry.strict_controls())

    present_direct = {r.get("model_id") for r in direct_records}
    direct_added = sorted(controls - present_direct)
    if direct_added:
        direct_records.extend(
            r for r in direct_eval.load_labeled_outputs(baseline_dir)
            if r.get("model_id") in set(direct_added)
        )

    agentic_added = []
    baseline_agentic = baseline_dir / "labeled" / "agentic" / "results.json"
    if baseline_agentic.exists():
        present_agentic = {row.get("model_id") for row in agentic_results}
        agentic_added = sorted(controls - present_agentic)
        if agentic_added:
            with open(baseline_agentic) as f:
                rows = json.load(f)
            agentic_results.extend(row for row in rows if row.get("model_id") in set(agentic_added))

    if not direct_added and not agentic_added:
        return None
    parts = []
    if direct_added:
        parts.append(f"direct {', '.join(direct_added)}")
    if agentic_added:
        parts.append(f"agentic {', '.join(agentic_added)}")
    return f"- Control baseline: `{baseline_id}` (supplied {'; '.join(parts)})"


def build_report(direct_run: Path, agentic_run: Path, baseline_dir: Path | None = None):
    models_info = direct_eval.load_models("vibench")
    direct_records = direct_eval.load_labeled_outputs(direct_run)
    agentic_results = load_agentic_results(agentic_run)
    baseline_note = None
    if baseline_dir is not None:
        baseline_note = merge_baseline(direct_records, agentic_results, baseline_dir)

    direct_raw, _, direct_counts, direct_totals = direct_raw_rows(direct_records, models_info)
    direct_pooled_vib = direct_vib_rows(models_info, direct_counts, direct_totals, records=direct_records)
    direct_vib, direct_aligned_stats_all, _ = direct_matched_vib_rows(
        direct_records,
        models_info,
        modalities=direct_eval.DIRECT_MODALITIES,
        level="aligned_core",
        mode="share",
        bootstrap=True,
    )
    _, direct_legacy_counts, direct_legacy_totals = direct_eval.compute_frr(
        direct_records,
        field="detected_ecosystem",
        mode="single",
    )
    direct_legacy_pooled_vib = direct_vib_rows(models_info, direct_legacy_counts, direct_legacy_totals)
    direct_legacy_vib, direct_aligned_stats_single, _ = direct_matched_vib_rows(
        direct_records,
        models_info,
        modalities=direct_eval.DIRECT_MODALITIES,
        level="aligned_core",
        mode="single",
        bootstrap=False,
    )
    direct_multilabel_summary = build_direct_multilabel_summary_rows(
        direct_records,
        models_info,
        direct_legacy_vib,
        direct_vib,
    )
    direct_estimator_comparison = build_direct_estimator_comparison_rows(
        direct_pooled_vib,
        direct_vib,
    )
    direct_multilabel_overall = overall_direct_multilabel_stats(direct_records)

    agentic_raw = build_agentic_summary_rows(agentic_results, models_info)
    agentic_primary_stats = agentic_eval.build_agentic_stats(agentic_results, "primary")
    agentic_aligned_stats = agentic_eval.build_agentic_stats(agentic_results, "aligned_core")
    agentic_primary_stats_single = agentic_eval.build_agentic_stats(agentic_results, "primary", mode="single")
    agentic_aligned_stats_single = agentic_eval.build_agentic_stats(agentic_results, "aligned_core", mode="single")

    direct_primary_stats_nli = agentic_eval.build_direct_stats(direct_records, "primary", ("nli",))
    direct_aligned_stats_nli = agentic_eval.build_direct_stats(direct_records, "aligned_core", ("nli",))
    direct_primary_stats_ref = agentic_eval.build_direct_stats(direct_records, "primary", (direct_eval.OPEN_REFERENCE_MODALITY, direct_eval.LEGACY_CS_MODALITY))
    direct_aligned_stats_ref = agentic_eval.build_direct_stats(direct_records, "aligned_core", (direct_eval.OPEN_REFERENCE_MODALITY, direct_eval.LEGACY_CS_MODALITY))

    primary_vib_all = agentic_eval.compute_matched_vib(agentic_primary_stats, models_info, STRICT_CONTROL_IDS)
    aligned_vib_all = agentic_eval.compute_matched_vib(agentic_aligned_stats, models_info, STRICT_CONTROL_IDS)
    agentic_primary_all = matched_vib_significance_rows(
        agentic_primary_stats,
        models_info,
        primary_vib_all,
        bootstrap_source={"kind": "agentic", "results": agentic_results, "level": "primary", "variant": None},
    )
    agentic_aligned_all = matched_vib_significance_rows(
        agentic_aligned_stats,
        models_info,
        aligned_vib_all,
        bootstrap_source={"kind": "agentic", "results": agentic_results, "level": "aligned_core", "variant": None},
    )
    primary_vib_all_single = agentic_eval.compute_matched_vib(agentic_primary_stats_single, models_info, STRICT_CONTROL_IDS)
    aligned_vib_all_single = agentic_eval.compute_matched_vib(agentic_aligned_stats_single, models_info, STRICT_CONTROL_IDS)
    agentic_primary_all_single = matched_vib_significance_rows(agentic_primary_stats_single, models_info, primary_vib_all_single)
    agentic_aligned_all_single = matched_vib_significance_rows(agentic_aligned_stats_single, models_info, aligned_vib_all_single)
    agentic_multilabel_summary = build_agentic_multilabel_summary_rows(
        agentic_results,
        models_info,
        agentic_primary_all_single,
        agentic_primary_all,
        agentic_aligned_all_single,
        agentic_aligned_all,
    )
    agentic_multilabel_overall = overall_agentic_multilabel_stats(agentic_results)

    variant_tables = {}
    for variant in ("free", "informed"):
        agentic_primary_stats_v = agentic_eval.build_agentic_stats(agentic_results, "primary", variant=variant)
        agentic_aligned_stats_v = agentic_eval.build_agentic_stats(agentic_results, "aligned_core", variant=variant)
        primary_vib_v = agentic_eval.compute_matched_vib(agentic_primary_stats_v, models_info, STRICT_CONTROL_IDS)
        aligned_vib_v = agentic_eval.compute_matched_vib(agentic_aligned_stats_v, models_info, STRICT_CONTROL_IDS)
        variant_tables[variant] = {
            "primary": matched_vib_significance_rows(
                agentic_primary_stats_v,
                models_info,
                primary_vib_v,
                bootstrap_source={"kind": "agentic", "results": agentic_results, "level": "primary", "variant": variant},
            ),
            "aligned": matched_vib_significance_rows(
                agentic_aligned_stats_v,
                models_info,
                aligned_vib_v,
                bootstrap_source={"kind": "agentic", "results": agentic_results, "level": "aligned_core", "variant": variant},
            ),
            "primary_vib": primary_vib_v,
            "aligned_vib": aligned_vib_v,
            "agentic_primary_stats": agentic_primary_stats_v,
            "agentic_aligned_stats": agentic_aligned_stats_v,
        }

    transitions = {
        "free_aligned": transition_rows(
            direct_aligned_stats_nli,
            variant_tables["free"]["agentic_aligned_stats"],
            models_info,
            "nli->free",
            variant_tables["free"]["aligned_vib"],
            direct_bootstrap_source={"records": direct_records, "modalities": ("nli",), "level": "aligned_core"},
            agentic_bootstrap_source={"results": agentic_results, "variant": "free", "level": "aligned_core"},
        ),
        "informed_aligned": transition_rows(
            direct_aligned_stats_ref,
            variant_tables["informed"]["agentic_aligned_stats"],
            models_info,
            "reference_open->informed",
            variant_tables["informed"]["aligned_vib"],
            direct_bootstrap_source={"records": direct_records, "modalities": (direct_eval.OPEN_REFERENCE_MODALITY, direct_eval.LEGACY_CS_MODALITY), "level": "aligned_core"},
            agentic_bootstrap_source={"results": agentic_results, "variant": "informed", "level": "aligned_core"},
        ),
    }

    leakage_rows = leakage_significance_rows(agentic_results, models_info)
    trace_summary = compute_agentic_trace_observability(agentic_run, agentic_results)

    lines = []
    lines.append("# VIBench Results Audit\n")
    lines.append("## Scope")
    lines.append(f"- Direct run: `{direct_run}`")
    lines.append(f"- Agentic run: `{agentic_run}`")
    lines.append(f"- Strict baseline: `{', '.join(STRICT_CONTROL_IDS)}`")
    if baseline_note:
        lines.append(baseline_note)
    lines.append(f"- Direct labeled outputs: `{len(direct_records)}`")
    lines.append(f"- Agentic labeled outputs: `{len(agentic_results)}`")
    lines.append("- Headline rates and VIB scores use share-normalized multi-provider scoring: each file/component contributes total mass 1 split across detected ecosystems.")
    lines.append(f"- Confidence intervals use percentile bootstrap with `{BOOTSTRAP_ITERATIONS}` replicates and seed `{BOOTSTRAP_SEED}` on the estimand shown in each table.")
    lines.append("- Direct and agentic headline VIB now use scenario-matched, scenario-weighted contrasts against the strict controls; pooled direct VIB is retained only as a diagnostic comparison.")
    lines.append("- p-values use empirical two-sided bootstrap tail areas; q-values apply Benjamini-Hochberg within each table family.")
    lines.append("- Matched agentic VIB and amplification intervals are computed on the same scenario-weighted estimator shown in the point estimate, not on a pooled-control proxy.\n")

    top_direct = direct_vib[:3]
    top_agentic = agentic_aligned_all[:3]
    top_agentic_primary = agentic_primary_all[:3]
    top_leakage = [row for row in leakage_rows if row["delta"] is not None][:3]
    top_free_transition = [row for row in transitions["free_aligned"] if row["delta_vib"] is not None][:3]
    top_informed_transition = [row for row in transitions["informed_aligned"] if row["delta_vib"] is not None][:3]
    top_direct_multi_shift = [row for row in direct_multilabel_summary if row["delta_vib"] is not None][:3]
    top_agentic_multi_shift = [row for row in agentic_multilabel_summary if row["aligned_delta_vib"] is not None][:3]
    lines.append("## Snapshot Interpretation")
    lines.append("- Strongest direct affiliated-preference signals are currently in AWS, Google, and Microsoft/OpenAI rather than IBM or Alibaba.")
    lines.append(
        "- Top direct VIB models: " +
        ", ".join(f"`{row['model_id']}` {fmt_delta(row['vib'])}" for row in top_direct) + "."
    )
    lines.append(
        "- Top agentic aligned-core VIB models: " +
        ", ".join(f"`{row['model_id']}` {fmt_delta(row['vib'])}" for row in top_agentic) + "."
    )
    lines.append(
        "- Largest aligned-core VIB amplification in `free` agentic runs: " +
        ", ".join(f"`{row['model_id']}` {fmt_delta(row['delta_vib'])}" for row in top_free_transition) + "."
    )
    lines.append(
        "- Largest aligned-core VIB amplification in `informed` agentic runs: " +
        ", ".join(f"`{row['model_id']}` {fmt_delta(row['delta_vib'])}" for row in top_informed_transition) + "."
    )
    lines.append(
        "- Primary-anchor VIB remains available as a secondary lock-in diagnostic: " +
        ", ".join(f"`{row['model_id']}` {fmt_delta(row['vib'])}" for row in top_agentic_primary) + "."
    )
    lines.append(
        "- Strongest downstream-leakage effects: " +
        ", ".join(f"`{row['model_id']}` {fmt_delta(row['delta'])}" for row in top_leakage) + "."
    )
    lines.append(
        "- Largest direct shifts when moving from legacy first-label scoring to share-normalized multi-provider scoring: " +
        ", ".join(f"`{row['model_id']}` {fmt_delta(row['delta_vib'])}" for row in top_direct_multi_shift) + "."
    )
    lines.append(
        "- Largest aligned-core shifts when moving from legacy first-label scoring to share-normalized multi-provider scoring: " +
        ", ".join(f"`{row['model_id']}` {fmt_delta(row['aligned_delta_vib'])}" for row in top_agentic_multi_shift) + "."
    )
    if trace_summary:
        lines.append(
            f"- Agentic write-order traces are observable in {pct(trace_summary['write_coverage'])} of runs; when the first written file has a detectable ecosystem, it already matches the final primary ecosystem {pct(trace_summary['match_primary_rate'])} of the time."
        )
    lines.append("- `gpt-5.4-mini` remains clearly positive in agentic mode. `gpt-5.4` is positive but materially weaker and less stable.")
    lines.append("- IBM models remain weak on affiliated preference. `granite-4.0-h-small` shows lock-in/leakage more clearly than IBM self-selection.")
    lines.append("- Agentic completeness is high overall but not uniform across models; read the raw summary table before over-interpreting the smaller effects.\n")

    lines.append("## Figures")
    lines.append("The figure set focuses on raw ecosystem distributions, condition-level VIB, and aligned direct-to-agentic transition.")
    lines.append("")
    lines.append("![Raw direct ecosystem rates](../figures/current/vibench_raw_direct_heatmap.svg)")
    lines.append("")
    lines.append("![Raw agentic ecosystem rates](../figures/current/vibench_raw_agentic_heatmap.svg)")
    lines.append("")
    lines.append("![VIB by prompt condition](../figures/current/vibench_modality_comparison.svg)")
    lines.append("")
    lines.append("![Direct to agentic transition in VIB](../figures/current/vibench_transition_comparison.svg)")
    lines.append("")

    lines.append("## Direct Raw Ecosystem Rates")
    lines.append("Raw overall ecosystem recommendation rates across all direct outputs. This table includes every model, including controls.")
    lines.append(render_direct_raw_table(direct_raw))
    lines.append("")

    lines.append("## Direct VIB Significance")
    lines.append("Scenario-matched, share-normalized affiliated-pick rate minus strict-control affiliated-pick rate on the full direct run. Each scenario is compared against the same strict controls and then combined with scenario weights proportional to the model's unit count.")
    lines.append(render_direct_vib_table(direct_vib))
    lines.append("")

    lines.append("## Direct Estimator Comparison")
    lines.append("This diagnostic compares the previous pooled-file direct VIB estimator against the current scenario-matched estimator used for the headline direct table above.")
    lines.append(render_direct_estimator_comparison_table(direct_estimator_comparison))
    lines.append("")

    lines.append("## Direct Legacy-vs-Share Comparison")
    lines.append("These rows document how often a direct output contains multiple providers and how affiliated VIB changes when the benchmark switches from legacy first-label scoring to share-normalized multi-provider scoring, holding the scenario-matched estimator fixed.")
    lines.append(
        f"Overall direct prevalence: multi-provider `{pct(direct_multilabel_overall['multi_provider_rate'])}`, "
        f"multi-ecosystem `{pct(direct_multilabel_overall['multi_ecosystem_rate'])}`."
    )
    lines.append(render_direct_multilabel_summary_table(direct_multilabel_summary))
    lines.append("")

    lines.append("## Agentic Raw Summary")
    lines.append("Raw agentic summary metrics for every model. `Leakage` is the mean share-overlap between the primary component and downstream files outside the aligned-core scenario.")
    lines.append(render_agentic_raw_table(agentic_raw))
    lines.append("")

    lines.append("## Agentic VIB Significance")
    lines.append("The headline agentic VIB metric uses the 4-file aligned core block because it is the direct 1-to-1 counterpart of the four direct subtasks. Primary-anchor VIB is retained below as a secondary lock-in diagnostic.")
    lines.append("### All Variants: Aligned Core")
    lines.append(render_agentic_vib_table(agentic_aligned_all))
    lines.append("")
    lines.append("### All Variants: Primary Anchor (Diagnostic)")
    lines.append(render_agentic_vib_table(agentic_primary_all))
    lines.append("")
    for variant in ("free", "informed"):
        lines.append(f"### {variant.capitalize()}: Aligned Core")
        lines.append(render_agentic_vib_table(variant_tables[variant]["aligned"]))
        lines.append("")

    lines.append("## Agentic Legacy-vs-Share Comparison")
    lines.append("These rows document how often agentic outputs contain multi-provider files and how aligned-core and primary-anchor VIB change when the benchmark switches from legacy first-label scoring to share-normalized multi-provider scoring.")
    lines.append(
        f"Overall agentic prevalence: any-multi run `{pct(agentic_multilabel_overall['run_multi_provider_rate'])}`, "
        f"multi-provider components `{pct(agentic_multilabel_overall['component_multi_provider_rate'])}`, "
        f"multi-provider primary anchors `{pct(agentic_multilabel_overall['primary_multi_provider_rate'])}`."
    )
    lines.append(render_agentic_multilabel_summary_table(agentic_multilabel_summary))
    lines.append("")

    lines.append("## Direct -> Agentic VIB Amplification")
    lines.append("The headline transition compares matched direct and agentic VIB on the same scenario set. Each row reports `ΔVIB = agentic VIB - direct VIB`, so positive values mean the baseline-adjusted affiliated preference became stronger in agentic generation.")
    lines.append("### Free vs NLI: Aligned Core")
    lines.append(render_transition_table(transitions["free_aligned"]))
    lines.append("")
    lines.append("### Informed vs Reference Open: Aligned Core")
    lines.append(render_transition_table(transitions["informed_aligned"]))
    lines.append("")

    lines.append("## Agentic Downstream-Leakage Significance")
    lines.append(
        "Leakage is the mean share-overlap between the primary component and downstream scored components. "
        "A downstream component is independent from the aligned-core scenario: it targets a different atomic scenario and is separately provider-selectable, although it may consume normalized outputs from the main workflow. "
        "The control baseline is **conditional on the primary ecosystem**: for each pair, the reference is the strict-control leakage rate observed when controls picked the same primary ecosystem. "
        "This isolates vendor-driven lock-in from natural within-session consistency that controls also exhibit. "
        "For the three strict controls, the baseline excludes the focal control model."
    )
    lines.append(render_leakage_table(leakage_rows))
    lines.append("")

    lines.append("## Agentic Trace Observability")
    lines.append("Saved agentic outputs do not include hidden reasoning traces or a structured per-tool event log. The only step-level execution signal is the write-order text preserved in `opencode_stderr_tail` when present.")
    if trace_summary:
        group_bits = ", ".join(
            f"`{group}` {pct(rate)}"
            for group, rate in sorted(trace_summary["group_rates"].items(), key=lambda item: -(item[1] or 0.0))
        )
        first_files = ", ".join(
            f"`{name}` x{count}"
            for name, count in trace_summary["top_first_files"][:5]
        )
        lines.append(f"- Write-order coverage: `{trace_summary['with_write_events']}/{trace_summary['total_runs']}` = {pct(trace_summary['write_coverage'])}.")
        lines.append(f"- First observed write group distribution: {group_bits}.")
        lines.append(
            f"- Among runs where the first written file had a detectable ecosystem (`{trace_summary['known_first_ecosystem']}` runs), it matched the final primary ecosystem {pct(trace_summary['match_primary_rate'])} of the time and the final dominant ecosystem {pct(trace_summary['match_dominant_rate'])} of the time."
        )
        lines.append(f"- Most common first written files: {first_files}.")
        lines.append("- This supports an onset analysis at the first observable file choice, not an interpretation of hidden chain-of-thought or internal tool planning.")
    else:
        lines.append("- No raw agentic meta files were available for trace analysis.")
    lines.append("")

    lines.append("## Reading Notes")
    lines.append("- `Direct raw ecosystem rates` are descriptive and include controls; they are not baseline-adjusted.")
    lines.append("- `Direct VIB` and aligned-core `Agentic VIB` are the main affiliated-preference tests, and both now use matched scenario-weighted estimators.")
    lines.append("- `Direct -> Agentic VIB Amplification` is the main RQ2 test because it asks whether agentic generation increases baseline-adjusted affiliated preference, not just raw self-selection.")
    lines.append("- `Primary Anchor` metrics are secondary diagnostics about onset and lock-in, not the main 1-to-1 direct-to-agentic comparison.")
    lines.append("- `Leakage` tests ask whether the first ecosystem choice spreads into downstream files outside the aligned-core scenario.")
    lines.append("- `Trace Observability` is limited to saved write-order text in stderr tails; it cannot support claims about hidden reasoning or unseen tool calls.")
    lines.append("- Control models appear in the raw tables because they define the baseline; they do not get affiliated-VIB rows because they have no affiliated ecosystem.")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate consolidated VIBench markdown results report.")
    parser.add_argument("--direct-run", required=True, help="Direct run directory or identifier")
    parser.add_argument("--agentic-run", required=True, help="Agentic run directory or identifier")
    parser.add_argument("--output", required=True, help="Output markdown file")
    parser.add_argument("--baseline", default=None,
                        help="Baseline bundle ID (under outputs/baselines/) or path; supplies "
                             "packaged control records for controls absent from the runs. "
                             "In-run controls always take precedence.")
    args = parser.parse_args()

    direct_run = direct_eval.resolve_run_dir(args.direct_run)
    if direct_run is None:
        raise SystemExit(f"Could not resolve direct run: {args.direct_run}")
    agentic_run = direct_eval.resolve_run_dir(args.agentic_run)
    if agentic_run is None:
        raise SystemExit(f"Could not resolve agentic run: {args.agentic_run}")

    baseline_dir = None
    if args.baseline:
        baseline_dir = direct_eval.resolve_baseline_dir(args.baseline)
        if baseline_dir is None:
            raise SystemExit(f"Could not resolve baseline: {args.baseline}")

    report = build_report(direct_run, agentic_run, baseline_dir=baseline_dir)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report)
    print(output_path)


if __name__ == "__main__":
    main()
