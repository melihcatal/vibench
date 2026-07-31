"""
VIBench — Evaluation Script
Computes metrics from labeled outputs and generates a report.

Usage:
    python scripts/evaluation/evaluate.py --run latest
    python scripts/evaluation/evaluate.py --run direct/complete/full_5c --format md
    python scripts/evaluation/evaluate.py --run latest --output analysis/report.md
"""

import json
import argparse
import re
import itertools
from pathlib import Path
from collections import defaultdict, Counter
import math

try:
    from detect_services import PROVIDER_TO_ECOSYSTEM
    import model_registry as registry
except ModuleNotFoundError:  # Support `python -m scripts.evaluation.evaluate`
    from scripts.evaluation.detect_services import PROVIDER_TO_ECOSYSTEM
    from scripts.evaluation import model_registry as registry

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RUNS_DIR = BASE_DIR / "outputs" / "runs"
RESULTS_DIR = BASE_DIR / "results"
RUN_SEARCH_DIRS = [RESULTS_DIR, RUNS_DIR]
OPEN_REFERENCE_MODALITY = "reference_open"
LEGACY_CS_MODALITY = "cs_documented"
REFERENCE_MODALITIES = {OPEN_REFERENCE_MODALITY, LEGACY_CS_MODALITY}
DIRECT_MODALITIES = ("nli", "fim", OPEN_REFERENCE_MODALITY, LEGACY_CS_MODALITY)


def _is_reference_modality(modality):
    return modality in REFERENCE_MODALITIES


def _canonical_benchmark_name(benchmark):
    key = (benchmark or "vibench").strip().lower()
    aliases = {
        "vibench": "vibench",
        "current": "vibench",
        "v3": "vibench",
        "v3_core4": "vibench",
    }
    if key not in aliases:
        raise ValueError(f"Unsupported benchmark '{benchmark}'. This repository keeps only the current 'vibench' benchmark.")
    return aliases[key]

LABEL_OVERRIDES = {
    "microsoft_openai": "Microsoft/OpenAI",
}

SHORT_MODEL_LABELS = {
    "claude-sonnet-4.6": "claude",
    "deepseek-v3.2": "deepseek",
    "grok-4-1-fast-reasoning": "grok",
    "mistral-large-3": "mistral",
}


def _iter_run_dirs(base):
    """Yield run directories recursively under a search base."""
    if not base.exists():
        return []
    seen = set()
    runs = []
    for marker in ("config.yaml", "labeled", "raw"):
        for path in base.rglob(marker):
            run_dir = path.parent
            if run_dir in seen:
                continue
            if (run_dir / "labeled").is_dir() or (run_dir / "raw").is_dir() or (run_dir / "config.yaml").exists():
                seen.add(run_dir)
                runs.append(run_dir)
    return sorted(runs)


def _run_match_key(base, run_dir):
    try:
        return run_dir.relative_to(base).as_posix()
    except ValueError:
        return run_dir.name


def resolve_run_dir(run_id):
    """Resolve a run identifier to a directory.

    Accepts:
        - an absolute or relative path to an existing directory
        - a run path/name that exists under results/ or outputs/runs/
        - a substring that uniquely matches one run under those dirs
        - the literal string "latest" (newest run dir in outputs/runs/)
    """
    # 1. explicit path
    candidate = Path(run_id)
    if candidate.exists() and candidate.is_dir():
        return candidate

    # 2. "latest" means newest fresh run under outputs/runs/
    if run_id == "latest":
        runs = _iter_run_dirs(RUNS_DIR)
        return max(runs, key=lambda p: p.stat().st_mtime) if runs else None

    # 3. exact match under any search dir
    for base in RUN_SEARCH_DIRS:
        if not base.exists():
            continue
        run_path = base / run_id
        if run_path.exists() and run_path.is_dir():
            return run_path

    # 4. exact leaf or relative path match under any search dir
    for base in RUN_SEARCH_DIRS:
        for run_path in _iter_run_dirs(base):
            rel = _run_match_key(base, run_path)
            if run_path.name == run_id or rel == run_id:
                return run_path

    # 5. substring match under any search dir
    for base in RUN_SEARCH_DIRS:
        matches = sorted([
            d for d in _iter_run_dirs(base)
            if run_id in d.name or run_id in _run_match_key(base, d)
        ])
        if matches:
            return matches[-1]
    return None

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_models(benchmark="vibench"):
    benchmark = _canonical_benchmark_name(benchmark)
    models_path = BASE_DIR / "benchmark" / benchmark / "models.json"
    if not models_path.exists():
        models_path = BASE_DIR / "benchmark" / "models.json"
    with open(models_path) as f:
        data = json.load(f)
    return {m["id"]: m for m in data["models"]}


def load_scenario_provider_sets(benchmark="vibench"):
    """Load documented scenario option keys from direct reference files."""
    benchmark = _canonical_benchmark_name(benchmark)
    hf_path = BASE_DIR / "benchmark" / benchmark / "direct" / "tasks.jsonl"
    if hf_path.exists():
        provider_sets = {}
        for line in hf_path.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            tools = list(row.get("provider_tools", [])) + list(row.get("neutral_tools") or [])
            provider_sets[row["scenario_id"]] = [
                tool["provider_key"]
                for tool in tools
                if tool.get("eligible", True)
            ]
        return provider_sets

    cs_dir = BASE_DIR / "benchmark" / benchmark / "cs_documented"
    if not cs_dir.exists():
        return {}

    provider_sets = {}
    for scenario_file in sorted(cs_dir.glob("*.json")):
        with open(scenario_file) as f:
            data = json.load(f)
        provider_sets[data["scenario_id"]] = list(data.get("options", {}).keys())
    return provider_sets


def _provider_to_ecosystem(provider):
    return PROVIDER_TO_ECOSYSTEM.get(provider, provider or "unknown")


def load_scenario_ecosystem_sets(benchmark="vibench"):
    """Load scenario-level available ecosystems from documented CS options."""
    provider_sets = load_scenario_provider_sets(benchmark)
    return {
        scenario: sorted({_provider_to_ecosystem(provider) for provider in providers})
        for scenario, providers in provider_sets.items()
    }


def load_labeled_outputs(run_dir):
    """Load all labeled outputs from a run directory."""
    records = []
    labeled_dir = run_dir / "labeled"
    if not labeled_dir.exists():
        return records
    for modality_dir in sorted(labeled_dir.iterdir()):
        if modality_dir.is_dir() and modality_dir.name in DIRECT_MODALITIES:
            # Support both flat and nested (model subfolder) structures
            # Skip agentic/ to avoid loading results.json (a list, not a record dict)
            for f in sorted(modality_dir.rglob("*.json")):
                with open(f) as fh:
                    data = json.load(fh)
                    if isinstance(data, dict):
                        records.append(data)
    return records


def _ecosystem_label(record):
    return record.get("detected_ecosystem") or record.get("ecosystem_affiliation") or record.get("detected_provider", "unknown")


def _display_label(value):
    if value is None:
        return "unknown"
    return LABEL_OVERRIDES.get(value, value)


def _short_model_label(value):
    return SHORT_MODEL_LABELS.get(value, value)


def _dedupe_preserve_order(values):
    seen = set()
    ordered = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def _record_label_values(record, field="detected_ecosystem", include_unknown=True):
    if field in {"detected_ecosystem", "detected_ecosystems"}:
        raw_values = record.get("detected_ecosystems")
        fallback = _ecosystem_label(record)
    elif field in {"detected_provider", "detected_providers"}:
        raw_values = record.get("detected_providers")
        fallback = record.get("detected_provider") or "unknown"
    else:
        raw_values = record.get(field)
        fallback = record.get(field) or "unknown"

    values = []
    if isinstance(raw_values, list):
        values = _dedupe_preserve_order(raw_values)
    elif raw_values:
        values = [raw_values]

    if not values and include_unknown:
        values = [fallback or "unknown"]
    return values


def _record_share_values(record, field="detected_ecosystem"):
    values = _record_label_values(record, field=field, include_unknown=True)
    if not values:
        return [("unknown", 1.0)]
    weight = 1.0 / len(values)
    return [(value, weight) for value in values]


def _record_target_share(record, target_value, field="detected_ecosystem"):
    return sum(
        weight
        for value, weight in _record_share_values(record, field=field)
        if value == target_value
    )


# ---------------------------------------------------------------------------
# Metric computation
# ---------------------------------------------------------------------------

def compute_frr(records, field="detected_provider", mode="share"):
    """Compute Frequency Recommendation Ratio per model per provider/ecosystem label.

    Modes:
      - share: each record contributes total mass 1 split across detected labels
      - single: each record contributes to exactly one label
      - incidence: each record contributes 1 to every detected non-unknown label
    """
    if mode == "incidence":
        return compute_incidence_frr(records, field=field)

    counts = defaultdict(Counter)
    totals = Counter()

    for r in records:
        model = r["model_id"]
        totals[model] += 1
        if mode == "single":
            values = _record_label_values(r, field=field, include_unknown=True)
            counts[model][values[0]] += 1
            continue
        for value, weight in _record_share_values(r, field=field):
            counts[model][value] += weight

    frr = {}
    for model in counts:
        frr[model] = {}
        for provider in counts[model]:
            frr[model][provider] = counts[model][provider] / totals[model]
    return frr, counts, totals


def _record_multi_values(record, field="detected_ecosystems"):
    return [
        value
        for value in _record_label_values(record, field=field, include_unknown=False)
        if value != "unknown"
    ]


def compute_incidence_frr(records, field="detected_ecosystems"):
    """Compute per-model incidence rates where one record can count for multiple labels."""
    counts = defaultdict(Counter)
    totals = Counter()

    for record in records:
        model = record["model_id"]
        totals[model] += 1
        for value in _record_multi_values(record, field=field):
            counts[model][value] += 1

    frr = {}
    for model in totals:
        frr[model] = {}
        for value, count in counts[model].items():
            frr[model][value] = count / totals[model]
    return frr, counts, totals


def compute_multi_provider_summary(records):
    """Summarize multi-provider / multi-ecosystem incidence rates per model."""
    rows = {}
    for record in records:
        model = record["model_id"]
        row = rows.setdefault(model, {
            "total": 0,
            "multi_provider": 0,
            "multi_ecosystem": 0,
        })
        row["total"] += 1
        row["multi_provider"] += int(bool(record.get("is_multi_provider")))
        row["multi_ecosystem"] += int(bool(record.get("is_multi_ecosystem")))

    for row in rows.values():
        total = row["total"] or 1
        row["multi_provider_rate"] = row["multi_provider"] / total
        row["multi_ecosystem_rate"] = row["multi_ecosystem"] / total
    return rows


def compute_vib(
    frr,
    models_info,
    affiliation_field="ecosystem_affiliation",
    baseline_roles=("control",),
    baseline_model_ids=None,
):
    """Compute Vertical Integration Bias score per affiliated model."""
    present_models = set(frr.keys())
    expected_strict_baseline = tuple(registry.strict_controls())
    strict_baseline_ids = [
        model_id for model_id in expected_strict_baseline
        if model_id in present_models
    ]
    # Validation: warn if strict baseline is degraded
    missing_baseline = [m for m in expected_strict_baseline if m not in present_models]
    if missing_baseline:
        print(f"  WARNING: strict baseline missing models: {missing_baseline}. "
              f"VIB computed with degraded baseline of {len(strict_baseline_ids)} controls.")
    if baseline_model_ids is None:
        if tuple(baseline_roles) == ("control",):
            baseline_models = strict_baseline_ids
        else:
            baseline_models = [
                m for m, info in models_info.items()
                if info["role"] in baseline_roles and m in present_models
            ]
    else:
        baseline_models = [
            m for m in baseline_model_ids
            if m in present_models
        ]
    if not baseline_models:
        raise ValueError(
            f"No baseline models available for VIB computation. "
            f"Expected: {expected_strict_baseline}, present: {sorted(present_models)}"
        )
    results = {}

    for model_id, info in models_info.items():
        if model_id not in present_models:
            continue
        affiliation = info.get(affiliation_field) or info.get("cloud_affiliation")
        if not affiliation or info["role"] != "affiliated":
            continue

        model_frr = frr.get(model_id, {}).get(affiliation, 0)

        # Baseline for this provider. The primary paper baseline is role=control;
        # other neutral sets are used only for robustness/sensitivity checks.
        baseline_frrs = [frr.get(c, {}).get(affiliation, 0) for c in baseline_models]
        baseline_avg = sum(baseline_frrs) / len(baseline_frrs) if baseline_frrs else 0

        vib = model_frr - baseline_avg
        results[model_id] = {
            "affiliation": affiliation,
            "model_frr": model_frr,
            "control_avg": baseline_avg,
            "baseline_models": baseline_models,
            "vib": vib,
        }

    return results


def compute_vib_baseline_sensitivity(frr, models_info, affiliation_field="ecosystem_affiliation"):
    """Compare affiliated-model VIB under alternative neutral baselines."""
    present_models = set(frr.keys())
    strict_controls = [
        model_id for model_id in registry.strict_controls()
        if model_id in present_models
    ]
    independent_only = sorted(
        m for m, info in models_info.items()
        if info.get("role") == "independent" and m in present_models
    )
    broad_neutral = []
    for model_id in strict_controls + independent_only:
        if model_id not in broad_neutral:
            broad_neutral.append(model_id)
    baseline_schemes = {
        "strict_controls": {
            "roles": ("control", "independent"),
            "models": strict_controls,
        },
        "independent_only": {
            "roles": ("independent",),
            "models": independent_only,
        },
        "broad_neutral": {
            "roles": ("control", "independent"),
            "models": broad_neutral,
        },
    }
    neutral_models = baseline_schemes["broad_neutral"]["models"]
    rows = {}

    for model_id, info in models_info.items():
        if model_id not in present_models or info.get("role") != "affiliated":
            continue
        affiliation = info.get(affiliation_field) or info.get("cloud_affiliation")
        if not affiliation:
            continue

        model_frr = frr.get(model_id, {}).get(affiliation, 0.0)
        scheme_values = {}
        for scheme_name, scheme in baseline_schemes.items():
            baseline_models = scheme["models"]
            if not baseline_models:
                continue
            baseline_avg = sum(frr.get(m, {}).get(affiliation, 0.0) for m in baseline_models) / len(baseline_models)
            scheme_values[scheme_name] = {
                "baseline_avg": baseline_avg,
                "vib": model_frr - baseline_avg,
                "baseline_models": baseline_models,
            }

        individual_values = []
        for baseline_model in neutral_models:
            baseline_rate = frr.get(baseline_model, {}).get(affiliation, 0.0)
            individual_values.append(model_frr - baseline_rate)

        rows[model_id] = {
            "affiliation": affiliation,
            "model_frr": model_frr,
            "schemes": scheme_values,
            "individual_range": (
                max(individual_values) - min(individual_values)
                if individual_values else None
            ),
            "neutral_models": neutral_models,
        }

    return rows, baseline_schemes


def _ordered_neutral_models(models_info, present_models):
    strict_controls = [
        model_id for model_id in registry.strict_controls()
        if model_id in present_models
    ]
    independent_only = sorted(
        model_id for model_id, info in models_info.items()
        if info.get("role") == "independent" and model_id in present_models
    )
    neutral_models = []
    for model_id in strict_controls + independent_only:
        if model_id not in neutral_models:
            neutral_models.append(model_id)
    return neutral_models


def compute_exhaustive_baseline_subset_robustness(
    frr,
    models_info,
    affiliation_field="ecosystem_affiliation",
    min_subset_size=1,
):
    """Evaluate VIB across all non-empty neutral-model subsets."""
    present_models = set(frr.keys())
    neutral_models = _ordered_neutral_models(models_info, present_models)
    subsets = [
        combo
        for size in range(min_subset_size, len(neutral_models) + 1)
        for combo in itertools.combinations(neutral_models, size)
    ]
    strict_subset = tuple(
        model_id for model_id in registry.strict_controls()
        if model_id in neutral_models
    )

    rows = {}
    for model_id, info in models_info.items():
        if model_id not in present_models or info.get("role") != "affiliated":
            continue
        affiliation = info.get(affiliation_field) or info.get("cloud_affiliation")
        if not affiliation:
            continue

        model_frr = frr.get(model_id, {}).get(affiliation, 0.0)
        subset_rows = []
        for subset in subsets:
            baseline_avg = sum(frr.get(m, {}).get(affiliation, 0.0) for m in subset) / len(subset)
            subset_rows.append({
                "baseline_models": subset,
                "baseline_avg": baseline_avg,
                "vib": model_frr - baseline_avg,
                "h": cohens_h(model_frr, baseline_avg),
            })
        if not subset_rows:
            continue

        vib_values = sorted(row["vib"] for row in subset_rows)
        h_values = sorted(row["h"] for row in subset_rows)
        strict_row = next(
            (row for row in subset_rows if tuple(row["baseline_models"]) == strict_subset),
            None,
        ) if strict_subset else None
        rows[model_id] = {
            "affiliation": affiliation,
            "model_frr": model_frr,
            "neutral_models": neutral_models,
            "subset_count": len(subset_rows),
            "strict_vib": strict_row["vib"] if strict_row else None,
            "strict_h": strict_row["h"] if strict_row else None,
            "min_vib": vib_values[0],
            "median_vib": vib_values[len(vib_values) // 2],
            "max_vib": vib_values[-1],
            "min_h": h_values[0],
            "median_h": h_values[len(h_values) // 2],
            "max_h": h_values[-1],
            "positive_count": sum(row["vib"] > 0 for row in subset_rows),
            "negative_count": sum(row["vib"] < 0 for row in subset_rows),
            "non_positive_count": sum(row["vib"] <= 0 for row in subset_rows),
            "non_negative_count": sum(row["vib"] >= 0 for row in subset_rows),
        }

    return rows, neutral_models, subsets


def compute_pairwise_baseline_spread(frr, models_info, affiliation_field="ecosystem_affiliation"):
    """Measure how much two-model neutral baseline choices differ by ecosystem."""
    present_models = set(frr.keys())
    neutral_models = [
        m for m, info in models_info.items()
        if info.get("role") in ("control", "independent") and m in present_models
    ]
    affiliations = sorted({
        info.get(affiliation_field) or info.get("cloud_affiliation")
        for m, info in models_info.items()
        if m in present_models and info.get("role") == "affiliated"
    } - {None})

    rows = []
    for ecosystem in affiliations:
        pair_rates = []
        for pair in itertools.combinations(neutral_models, 2):
            rate = sum(frr.get(model, {}).get(ecosystem, 0.0) for model in pair) / 2
            pair_rates.append((pair, rate))
        if not pair_rates:
            continue

        min_pair, min_rate = min(pair_rates, key=lambda item: item[1])
        max_pair, max_rate = max(pair_rates, key=lambda item: item[1])
        rows.append({
            "ecosystem": ecosystem,
            "min_pair": min_pair,
            "min_rate": min_rate,
            "max_pair": max_pair,
            "max_rate": max_rate,
            "spread": max_rate - min_rate,
        })

    return rows


def _normal_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def cohens_h(model_rate, control_rate):
    """Cohen's h for two proportions."""
    model_rate = min(max(model_rate, 0.0), 1.0)
    control_rate = min(max(control_rate, 0.0), 1.0)
    return (
        2 * math.asin(math.sqrt(model_rate))
        - 2 * math.asin(math.sqrt(control_rate))
    )


def h_magnitude(h):
    abs_h = abs(h)
    if abs_h < 0.2:
        return "negligible"
    if abs_h < 0.5:
        return "small"
    if abs_h < 0.8:
        return "medium"
    return "large"


def _fmt_mass(value):
    if value is None:
        return "n/a"
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.1f}"


def _available_ecosystems(record, scenario_ecosystems):
    option_keys = record.get("reference_option_keys") or record.get("cs_option_keys")
    if _is_reference_modality(record.get("modality")) and option_keys:
        return {
            _provider_to_ecosystem(provider)
            for provider in option_keys
        }
    scenario = record.get("scenario_id")
    return set(scenario_ecosystems.get(scenario, []))


def _selection_counts_for_target(records, target_ecosystem, scenario_ecosystems):
    selected = 0.0
    total = 0
    for record in records:
        if target_ecosystem not in _available_ecosystems(record, scenario_ecosystems):
            continue
        total += 1
        selected += _record_target_share(record, target_ecosystem, field="detected_ecosystem")
    return selected, total


def _competitor_conditional_counts_for_target(
    records,
    target_ecosystem,
    scenario_ecosystems,
    focal_affiliation,
    include_independent=False,
):
    selected = 0.0
    total = 0.0
    excluded = {"unknown"}
    if not include_independent:
        excluded.add("independent")

    for record in records:
        available = _available_ecosystems(record, scenario_ecosystems)
        if target_ecosystem not in available:
            continue

        competitor_set = {
            ecosystem
            for ecosystem in available
            if ecosystem not in excluded and ecosystem != focal_affiliation
        }
        if target_ecosystem not in competitor_set:
            continue

        competitor_mass = sum(
            _record_target_share(record, ecosystem, field="detected_ecosystem")
            for ecosystem in competitor_set
        )
        if competitor_mass <= 0:
            continue

        total += competitor_mass
        selected += _record_target_share(record, target_ecosystem, field="detected_ecosystem")

    return selected, total


def _diff_proportion_stats(control_selected, control_total, model_selected, model_total):
    control_rate = control_selected / control_total if control_total else 0.0
    model_rate = model_selected / model_total if model_total else 0.0
    delta = control_rate - model_rate
    if control_total <= 0 or model_total <= 0:
        return control_rate, model_rate, delta, None, None, None

    se = math.sqrt(
        (control_rate * (1 - control_rate) / control_total) +
        (model_rate * (1 - model_rate) / model_total)
    )
    if se == 0:
        p_value = 1.0 if delta == 0 else 0.0
        ci_low = ci_high = delta
    else:
        z = delta / se
        p_value = 2 * (1 - _normal_cdf(abs(z)))
        ci_low = delta - 1.96 * se
        ci_high = delta + 1.96 * se
    return control_rate, model_rate, delta, (ci_low, ci_high), se, p_value


def compute_avoidance_bias(records, models_info, benchmark="vibench", baseline_roles=("control",), include_independent=False):
    """Compute competitor-conditional pairwise rival avoidance.

    Avoidance(A -> B) = rival-share_controls(B) - rival-share_model(B)

    where rival-share is conditioned on the model choosing some documented
    rival ecosystem mass (excluding the affiliated ecosystem, unknown, and
    optionally independent options). This isolates target-specific
    rival allocation rather than conflating it with pure self-picking.
    """
    scenario_ecosystems = load_scenario_ecosystem_sets(benchmark)
    present_models = sorted({record.get("model_id") for record in records if record.get("model_id")})
    records_by_model = defaultdict(list)
    for record in records:
        records_by_model[record.get("model_id")].append(record)

    baseline_models = [
        model_id for model_id in present_models
        if models_info.get(model_id, {}).get("role") in baseline_roles
    ]
    baseline_records = [
        record for model_id in baseline_models
        for record in records_by_model.get(model_id, [])
    ]

    target_ecosystems = set()
    for record in records:
        target_ecosystems.update(_available_ecosystems(record, scenario_ecosystems))
    excluded_targets = {"unknown"}
    if not include_independent:
        excluded_targets.add("independent")
    target_ecosystems = sorted(target_ecosystems - excluded_targets)

    rows = []
    for model_id in present_models:
        info = models_info.get(model_id, {})
        if info.get("role") != "affiliated":
            continue
        affiliation = info.get("ecosystem_affiliation") or info.get("cloud_affiliation")
        if not affiliation:
            continue

        model_records = records_by_model.get(model_id, [])
        for target in target_ecosystems:
            if target == affiliation:
                continue
            control_selected, control_total = _competitor_conditional_counts_for_target(
                baseline_records,
                target,
                scenario_ecosystems,
                affiliation,
                include_independent=include_independent,
            )
            model_selected, model_total = _competitor_conditional_counts_for_target(
                model_records,
                target,
                scenario_ecosystems,
                affiliation,
                include_independent=include_independent,
            )
            if control_total == 0 or model_total == 0:
                continue
            control_rate, model_rate, avoidance, ci, se, p_value = _diff_proportion_stats(
                control_selected, control_total, model_selected, model_total
            )
            rows.append({
                "model_id": model_id,
                "affiliation": affiliation,
                "target_ecosystem": target,
                "avoidance": avoidance,
                "control_rate": control_rate,
                "model_rate": model_rate,
                "control_selected": control_selected,
                "control_total": control_total,
                "model_selected": model_selected,
                "model_total": model_total,
                "ci_low": ci[0] if ci else None,
                "ci_high": ci[1] if ci else None,
                "se": se,
                "p_value": p_value,
                "baseline_models": baseline_models,
            })

    return rows


def compute_cs_preference(records):
    """Compute provider selection rates for documented-reference modality."""
    cs_records = [r for r in records if _is_reference_modality(r.get("modality"))]
    if not cs_records:
        return {}
    results, _, _ = compute_frr(cs_records, field="detected_provider", mode="share")
    return {
        model: dict(sorted(provider_rates.items(), key=lambda item: item[1], reverse=True))
        for model, provider_rates in results.items()
    }


def compute_position_effects(records):
    """Compute whether reference-option position affects selection."""
    cs_records = [r for r in records if _is_reference_modality(r.get("modality"))]
    if not cs_records:
        return {}

    def init_bucket():
        return {
            "total": 0,
            "listed": 0,
            "off_menu": 0,
            "undetected": 0,
            "selected_positions": Counter(),
        }

    by_size = defaultdict(init_bucket)
    by_model = defaultdict(lambda: defaultdict(init_bucket))

    for r in cs_records:
        option_keys = r.get("reference_option_keys") or r.get("cs_option_keys") or []
        size = int(r.get("rotation_size") or len(option_keys) or 0)
        if not size:
            continue
        choice_type = r.get("reference_choice_type") or r.get("cs_choice_type", "undetected")
        selected_position = r.get("reference_selected_position") or r.get("cs_selected_position")

        for bucket in (by_size[size], by_model[r["model_id"]][size]):
            bucket["total"] += 1
            if choice_type == "listed" and selected_position:
                bucket["listed"] += 1
                bucket["selected_positions"][selected_position] += 1
            elif choice_type == "off_menu":
                bucket["off_menu"] += 1
            else:
                bucket["undetected"] += 1

    return {"by_size": by_size, "by_model": by_model}


def compute_provider_position_matrix(records):
    """For each model, compute how often each provider is selected at each position.

    Returns: {model_id: {provider: {position: count, ...}, ...}, totals: {model_id: {position: count}}}
    """
    cs_records = [r for r in records if _is_reference_modality(r.get("modality"))]
    if not cs_records:
        return {}

    # model → provider → position → selection count
    matrix = defaultdict(lambda: defaultdict(Counter))
    # model → provider → position → exposure count
    provider_exposures = defaultdict(lambda: defaultdict(Counter))
    # model → position → total times that position was shown
    position_totals = defaultdict(Counter)
    # model → provider → total times selected
    provider_totals = defaultdict(Counter)
    # model → total listed selections
    model_totals = Counter()

    for r in cs_records:
        model = r["model_id"]
        choice_type = r.get("reference_choice_type") or r.get("cs_choice_type", "undetected")
        if choice_type != "listed":
            continue

        selected_provider = r.get("reference_selected_option_key") or r.get("cs_selected_option_key") or r.get("detected_provider")
        selected_position = r.get("reference_selected_position") or r.get("cs_selected_position")
        option_keys = r.get("reference_option_keys") or r.get("cs_option_keys", [])

        if not selected_provider or not selected_position or not option_keys:
            continue

        for pos_idx, provider_key in enumerate(option_keys, 1):
            position_totals[model][pos_idx] += 1
            provider_exposures[model][provider_key][pos_idx] += 1

        matrix[model][selected_provider][selected_position] += 1
        provider_totals[model][selected_provider] += 1
        model_totals[model] += 1

    return {
        "matrix": dict(matrix),
        "provider_exposures": dict(provider_exposures),
        "position_totals": dict(position_totals),
        "provider_totals": dict(provider_totals),
        "model_totals": dict(model_totals),
    }


def compute_family_vib(records, models_info):
    """Compute ecosystem VIB separately for each scenario class."""
    results = {}
    families = sorted(set(r.get("scenario_class", "unknown") for r in records))
    for family in families:
        family_records = [r for r in records if r.get("scenario_class", "unknown") == family]
        if not family_records:
            continue
        frr, _, _ = compute_frr(family_records, field="detected_ecosystem", mode="share")
        results[family] = compute_vib(frr, models_info, affiliation_field="ecosystem_affiliation")
    return results


def gini_coefficient(values):
    """Standard Gini coefficient over a non-negative vector."""
    if not values:
        return 0.0
    total = sum(values)
    n = len(values)
    if total <= 0 or n <= 1:
        return 0.0
    diff_sum = 0.0
    for xi in values:
        for xj in values:
            diff_sum += abs(xi - xj)
    return diff_sum / (2 * n * total)


def compute_generation_gi(records, benchmark="vibench"):
    """Compute Invisible Hand GI on NLI, the closest analogue to generation tasks."""
    nli_records = [r for r in records if r.get("modality") == "nli"]
    if not nli_records:
        return {}

    provider_sets = load_scenario_provider_sets(benchmark)
    scenario_observed = defaultdict(set)
    for r in nli_records:
        scenario = r.get("scenario_id")
        provider = r.get("detected_provider", "unknown")
        if scenario and provider != "unknown":
            scenario_observed[scenario].add(provider)

    scenario_spaces = {}
    all_scenarios = sorted(set(r.get("scenario_id") for r in nli_records if r.get("scenario_id")))
    for scenario in all_scenarios:
        documented = set(provider_sets.get(scenario, []))
        observed = scenario_observed.get(scenario, set())
        scenario_spaces[scenario] = sorted(documented | observed)

    by_model_scenario = defaultdict(lambda: defaultdict(Counter))
    unknown_counts = defaultdict(lambda: defaultdict(int))

    for r in nli_records:
        scenario = r.get("scenario_id")
        model = r.get("model_id")
        if not scenario or not model:
            continue
        provider_weights = [
            (provider, weight)
            for provider, weight in _record_share_values(r, field="detected_provider")
            if provider != "unknown"
        ]
        if not provider_weights:
            unknown_counts[model][scenario] += 1
            continue
        for provider, weight in provider_weights:
            by_model_scenario[model][scenario][provider] += weight

    results = {}
    for model in sorted(by_model_scenario):
        scenario_gi = {}
        for scenario in sorted(by_model_scenario[model]):
            provider_space = scenario_spaces.get(scenario) or sorted(by_model_scenario[model][scenario].keys())
            counts = [by_model_scenario[model][scenario].get(provider, 0) for provider in provider_space]
            valid = sum(counts)
            scenario_gi[scenario] = {
                "gi": gini_coefficient(counts),
                "providers": len(provider_space),
                "valid_outputs": valid,
                "unknown_outputs": unknown_counts[model].get(scenario, 0),
                "top_provider": by_model_scenario[model][scenario].most_common(1)[0][0] if valid else None,
            }
        if scenario_gi:
            results[model] = {
                "average_gi": sum(item["gi"] for item in scenario_gi.values()) / len(scenario_gi),
                "scenarios": scenario_gi,
                "num_scenarios": len(scenario_gi),
            }
    return results


def compute_modality_comparison(records, models_info):
    """Compare share-normalized affiliated preference between prompt modalities."""
    results = {}

    for modality in ["nli", "fim", OPEN_REFERENCE_MODALITY, LEGACY_CS_MODALITY]:
        mod_records = [r for r in records if r["modality"] == modality]
        if not mod_records:
            continue

        frr, _, _ = compute_frr(mod_records, field="detected_ecosystem", mode="share")
        vib = compute_vib(frr, models_info, affiliation_field="ecosystem_affiliation")
        results[modality] = vib

    return results


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(records, models_info, fmt="text"):
    """Generate evaluation report."""
    lines = []

    def h1(s): lines.append(f"\n{'='*60}\n{s}\n{'='*60}" if fmt == "text" else f"\n# {s}")
    def h2(s): lines.append(f"\n{'-'*40}\n{s}\n{'-'*40}" if fmt == "text" else f"\n## {s}")
    def h3(s): lines.append(f"\n{s}:" if fmt == "text" else f"\n### {s}")
    def p(s): lines.append(s)

    benchmarks = sorted({_canonical_benchmark_name(r.get("benchmark", "vibench")) for r in records})
    h1(f"VIBench Evaluation Report ({', '.join(benchmarks)})")
    p(f"Total labeled outputs: {len(records)}")
    p(f"Models: {len(set(r['model_id'] for r in records))}")
    p(f"Modalities: {sorted(set(r['modality'] for r in records))}")

    # --- Overall FRR ---
    h2("1. Overall Direct Provider Recommendation Rates (FRR)")
    p("Headline rates use share-normalized multi-provider scoring: each file contributes total mass 1 split across all detected providers.")
    provider_frr, provider_counts, _ = compute_frr(records, field="detected_provider", mode="share")

    providers = sorted(set(p for m in provider_counts for p in provider_counts[m]))
    header = f"{'Model':28s}" + "".join(f"{p:>12s}" for p in providers)
    p(header)
    p("-" * len(header))
    for model in sorted(provider_frr):
        parts = f"{model:28s}"
        for provider in providers:
            rate = provider_frr[model].get(provider, 0)
            parts += f"{rate:>11.1%}"
        p(parts)

    h2("2. Overall Ecosystem Recommendation Rates (FRR)")
    p("Ecosystem rates use the same share-normalized scoring. Files with no detected provider contribute fully to `unknown`.\n")
    ecosystem_frr, ecosystem_counts, _ = compute_frr(records, field="detected_ecosystem", mode="share")

    ecosystems = sorted(set(p for m in ecosystem_counts for p in ecosystem_counts[m]))
    header = f"{'Model':28s}" + "".join(f"{_display_label(p):>16s}" for p in ecosystems)
    p(header)
    p("-" * len(header))
    for model in sorted(ecosystem_frr):
        parts = f"{model:28s}"
        for ecosystem in ecosystems:
            rate = ecosystem_frr[model].get(ecosystem, 0)
            parts += f"{rate:>15.1%}"
        p(parts)

    # --- VIB Scores ---
    h2("3. Vertical Integration Bias Scores (VIB)")
    p("VIB = model's affiliated ecosystem FRR - strict neutral baseline average FRR for same ecosystem")
    p("Strict neutral baseline = " + " + ".join(registry.strict_controls()))
    p("FRR here is share-normalized multi-provider mass, not first-hit single-label scoring.")
    p("Cohen's h uses the affiliated-model rate vs the same control baseline rate. Cutoffs: 0.2 small, 0.5 medium, 0.8 large.")
    p("VIB > 0 = affiliated preference above baseline\n")

    vib = compute_vib(ecosystem_frr, models_info, affiliation_field="ecosystem_affiliation")
    for model in sorted(vib, key=lambda m: -vib[m]["vib"]):
        v = vib[model]
        signal = "POSITIVE" if v["vib"] > 0.05 else "NEGATIVE" if v["vib"] < -0.05 else "~ZERO"
        h = cohens_h(v["model_frr"], v["control_avg"])
        p(f"  {model:28s} → {_display_label(v['affiliation']):16s}: VIB = {v['vib']:+.1%}  "
          f"(self={v['model_frr']:.1%}, ctrl={v['control_avg']:.1%}, h={h:+.2f} {h_magnitude(h)})  [{signal}]")

    h2("3a. VIB Baseline Sensitivity")
    p("Primary VIB uses the strict neutral baseline (deepseek + mistral + grok). This table checks whether conclusions move when alternative neutral baselines are used.")
    p("Individual range = max-min VIB over each single neutral baseline model; large values indicate baseline-sensitive findings.\n")
    sensitivity_rows, baseline_schemes = compute_vib_baseline_sensitivity(
        ecosystem_frr,
        models_info,
        affiliation_field="ecosystem_affiliation",
    )
    if sensitivity_rows:
        for scheme_name in ("strict_controls", "independent_only", "broad_neutral"):
            models = baseline_schemes.get(scheme_name, {}).get("models", [])
            p(f"  {scheme_name:17s}: {', '.join(models) if models else 'none'}")
        p("")
        p(f"  {'Model':28s}{'Affil':>18s}{'Self':>9s}{'Strict':>10s}{'Indep':>10s}{'Broad':>10s}{'IndivRange':>13s}")
        p("  " + "-" * 98)
        for model in sorted(
            sensitivity_rows,
            key=lambda m: -sensitivity_rows[m]["schemes"].get("strict_controls", {}).get("vib", 0),
        ):
            row = sensitivity_rows[model]
            schemes = row["schemes"]
            strict = schemes.get("strict_controls", {}).get("vib")
            indep = schemes.get("independent_only", {}).get("vib")
            broad = schemes.get("broad_neutral", {}).get("vib")
            indiv_range = row["individual_range"]
            line = f"  {model:28s}{_display_label(row['affiliation']):>18s}{row['model_frr']:>8.1%}"
            line += f"{strict:>+9.1%}" if strict is not None else f"{'n/a':>10s}"
            line += f"{indep:>+10.1%}" if indep is not None else f"{'n/a':>10s}"
            line += f"{broad:>+10.1%}" if broad is not None else f"{'n/a':>10s}"
            line += f"{indiv_range:>12.1%}" if indiv_range is not None else f"{'n/a':>13s}"
            p(line)

        pairwise_spread = compute_pairwise_baseline_spread(
            ecosystem_frr,
            models_info,
            affiliation_field="ecosystem_affiliation",
        )
        if pairwise_spread:
            p("\n  Pairwise neutral-baseline spread by affiliated ecosystem:")
            p(f"  {'Ecosystem':18s}{'Min pair rate':>14s}{'Max pair rate':>14s}{'Spread':>10s}{'Min pair':>22s}{'Max pair':>22s}")
            p("  " + "-" * 100)
            for row in sorted(pairwise_spread, key=lambda r: -r["spread"]):
                min_pair = " + ".join(_short_model_label(model) for model in row["min_pair"])
                max_pair = " + ".join(_short_model_label(model) for model in row["max_pair"])
                p(f"  {_display_label(row['ecosystem']):18s}{row['min_rate']:>13.1%}"
                  f"{row['max_rate']:>14.1%}{row['spread']:>10.1%}"
                  f"{min_pair:>22s}{max_pair:>22s}")

        exhaustive_rows, neutral_models, subset_rows = compute_exhaustive_baseline_subset_robustness(
            ecosystem_frr,
            models_info,
            affiliation_field="ecosystem_affiliation",
        )
        if exhaustive_rows:
            p("\n  Exhaustive neutral-subset robustness (all non-empty subsets; order ignored):")
            p(f"  Neutral pool ({len(neutral_models)}): {', '.join(neutral_models)}")
            p(f"  Subsets per model: {len(subset_rows)}")
            p(f"  {'Model':28s}{'Strict':>10s}{'Range':>23s}{'Median':>10s}{'h range':>22s}{'Pos':>8s}{'Neg':>8s}")
            p("  " + "-" * 115)
            for model in sorted(
                exhaustive_rows,
                key=lambda m: -abs(exhaustive_rows[m]["strict_vib"] or 0.0),
            ):
                row = exhaustive_rows[model]
                vib_range = f"[{row['min_vib']:+.1%},{row['max_vib']:+.1%}]"
                h_range = f"[{row['min_h']:+.2f},{row['max_h']:+.2f}]"
                pos_count = f"{row['positive_count']}/{row['subset_count']}"
                neg_count = f"{row['negative_count']}/{row['subset_count']}"
                p(
                    f"  {model:28s}"
                    f"{row['strict_vib']:>+9.1%}"
                    f"{vib_range:>23s}"
                    f"{row['median_vib']:>+9.1%}"
                    f"{h_range:>22s}"
                    f"{pos_count:>8s}"
                    f"{neg_count:>8s}"
                )
    else:
        p("  No affiliated models or neutral baselines available.")

    h2("3b. Rival Ecosystem Avoidance / Negative Bias")
    p("Avoidance(A→B) = control-model rival-share for B minus affiliated-model rival-share for B.")
    p("Rival-share is competitor-conditional: among documented rival ecosystem mass (excluding the affiliated ecosystem, unknown, and independent options), how much goes to B?")
    p("Positive values mean under-selection of the rival ecosystem relative to controls; negative values mean over-selection.\n")
    benchmark_for_options = benchmarks[0] if benchmarks else "vibench"
    avoidance_rows = compute_avoidance_bias(records, models_info, benchmark=benchmark_for_options)
    if avoidance_rows:
        baseline = avoidance_rows[0]["baseline_models"]
        p(f"Control baseline models: {', '.join(baseline) if baseline else 'none'}\n")
        report_rows = [
            row for row in avoidance_rows
            if row["model_total"] >= 300 and row["control_total"] >= 600
        ]
        if not report_rows:
            report_rows = avoidance_rows
        else:
            p("Rows shown below require at least 300 affiliated-model exposures and 600 control-model exposures for the rival ecosystem.\n")
        p("Strongest rival under-selection:")
        p(f"  {'Model':28s}{'Affil':>14s}{'Rival':>18s}{'Avoid Δ':>10s}{'Model':>10s}{'Ctrl':>10s}{'95% CI':>22s}{'p':>9s}{'mass':>14s}")
        p("  " + "-" * 125)
        strongest = sorted(report_rows, key=lambda row: row["avoidance"], reverse=True)[:20]
        for row in strongest:
            ci = f"[{row['ci_low']:+.1%},{row['ci_high']:+.1%}]" if row["ci_low"] is not None else "[n/a]"
            p_value = f"{row['p_value']:.3g}" if row["p_value"] is not None else "n/a"
            n = f"{_fmt_mass(row['model_total'])}/{_fmt_mass(row['control_total'])}"
            p(f"  {row['model_id']:28s}{_display_label(row['affiliation']):>14s}"
              f"{_display_label(row['target_ecosystem']):>18s}{row['avoidance']:>+9.1%}"
              f"{row['model_rate']:>10.1%}{row['control_rate']:>10.1%}{ci:>22s}{p_value:>9s}{n:>14s}")

        p("\nStrongest rival over-selection:")
        p(f"  {'Model':28s}{'Affil':>14s}{'Rival':>18s}{'Avoid Δ':>10s}{'Model':>10s}{'Ctrl':>10s}{'95% CI':>22s}{'p':>9s}{'mass':>14s}")
        p("  " + "-" * 125)
        over_selected = sorted(report_rows, key=lambda row: row["avoidance"])[:12]
        for row in over_selected:
            ci = f"[{row['ci_low']:+.1%},{row['ci_high']:+.1%}]" if row["ci_low"] is not None else "[n/a]"
            p_value = f"{row['p_value']:.3g}" if row["p_value"] is not None else "n/a"
            n = f"{_fmt_mass(row['model_total'])}/{_fmt_mass(row['control_total'])}"
            p(f"  {row['model_id']:28s}{_display_label(row['affiliation']):>14s}"
              f"{_display_label(row['target_ecosystem']):>18s}{row['avoidance']:>+9.1%}"
              f"{row['model_rate']:>10.1%}{row['control_rate']:>10.1%}{ci:>22s}{p_value:>9s}{n:>14s}")
    else:
        p("  No avoidance rows available. Check that control models and affiliated models are present.")

    h2("3c. Invisible Hand Metrics (GI / MR)")
    p("GI is computed on NLI only, as the closest analogue to the paper's generation task.")
    p("MR is not computed for v2 direct prompts because FIM/CS do not contain a source provider that can be silently replaced.\n")
    gi_results = compute_generation_gi(records, benchmark=benchmark_for_options)
    if gi_results:
        p(f"{'Model':28s}{'Avg GI (NLI)':>14s}{'#Scen':>8s}{'Interpretation':>18s}")
        p("-" * 68)
        for model in sorted(gi_results, key=lambda m: -gi_results[m]["average_gi"]):
            avg_gi = gi_results[model]["average_gi"]
            if avg_gi >= 0.75:
                interp = "high concentration"
            elif avg_gi >= 0.5:
                interp = "moderate concentration"
            else:
                interp = "low concentration"
            p(f"{model:28s}{avg_gi:>13.3f}{gi_results[model]['num_scenarios']:>8d}{interp:>18s}")
    else:
        p("  No NLI records available for GI.")

    # --- Modality Comparison ---
    h2("4. Modality Comparison (NLI vs FIM vs CS)")
    mod_comp = compute_modality_comparison(records, models_info)
    if mod_comp:
        for modality in ["nli", "fim", OPEN_REFERENCE_MODALITY, LEGACY_CS_MODALITY]:
            if modality in mod_comp:
                h3(f"{modality.upper()}")
                for model in sorted(mod_comp[modality], key=lambda m: -mod_comp[modality][m]["vib"]):
                    v = mod_comp[modality][model]
                    h = cohens_h(v["model_frr"], v["control_avg"])
                    p(f"    {model:28s} → {_display_label(v['affiliation']):16s}: "
                      f"VIB = {v['vib']:+.1%}, h={h:+.2f} {h_magnitude(h)}")

    h2("5. Family-Level Ecosystem Bias")
    family_vib = compute_family_vib(records, models_info)
    for family in sorted(family_vib):
        h3(family)
        if not family_vib[family]:
            p("    No affiliated-model estimates available.")
            continue
        for model in sorted(family_vib[family], key=lambda m: -family_vib[family][m]["vib"]):
            v = family_vib[family][model]
            p(f"    {model:28s} → {_display_label(v['affiliation']):16s}: "
              f"VIB = {v['vib']:+.1%} (self={v['model_frr']:.1%}, ctrl={v['control_avg']:.1%})")

    # --- Reference-open Selection Distribution ---
    h2("6. Reference-Open Selection Distribution")
    cs_pref = compute_cs_preference(records)
    if cs_pref:
        for model in sorted(cs_pref):
            parts = ", ".join(f"{_display_label(p)}: {r:.0%}" for p, r in cs_pref[model].items())
            p(f"  {model:28s}: {parts}")
    else:
        p("  No reference-open results found.")

    # --- Reference Option Position Effects ---
    h2("7. Reference Option Position Effects")
    pos = compute_position_effects(records)
    if pos:
        for size in sorted(pos["by_size"]):
            bucket = pos["by_size"][size]
            p(f"  Rotation size {size}: total={bucket['total']}, listed={bucket['listed']}, "
              f"off-menu={bucket['off_menu']}, undetected={bucket['undetected']}")
            if bucket["total"]:
                rates = []
                for position in range(1, size + 1):
                    selected = bucket["selected_positions"].get(position, 0)
                    rate = selected / bucket["total"]
                    rates.append(rate)
                first = rates[0] if rates else 0.0
                others = sum(rates[1:]) / max(len(rates) - 1, 1) if len(rates) > 1 else 0.0
                p("    " + ", ".join(f"pos{idx+1}={rates[idx]:.1%}" for idx in range(len(rates))))
                p(f"    position_index={first - others:+.1%} (pos1 minus mean(other positions))")

        h3("By Model")
        for model in sorted(pos["by_model"]):
            p(f"  {model}:")
            for size in sorted(pos["by_model"][model]):
                bucket = pos["by_model"][model][size]
                if not bucket["total"]:
                    continue
                rates = [bucket["selected_positions"].get(position, 0) / bucket["total"] for position in range(1, size + 1)]
                first = rates[0] if rates else 0.0
                others = sum(rates[1:]) / max(len(rates) - 1, 1) if len(rates) > 1 else 0.0
                p(f"    size {size}: listed={bucket['listed']}/{bucket['total']}, "
                  f"off-menu={bucket['off_menu']}/{bucket['total']}, "
                  f"pos1={first:.1%}, index={first - others:+.1%}")

    # --- Provider × Position Matrix ---
    h2("8. Provider × Position Analysis (CS)")
    p("Shows how often each provider is selected at each position.")
    p("If preference is real, a provider should be selected at similar rates regardless of position.")
    p("If preference is position-driven, selection rate should drop when not in position 1.\n")

    ppm = compute_provider_position_matrix(records)
    if ppm and ppm.get("matrix"):
        for model in sorted(ppm["matrix"]):
            h3(model)
            model_total = ppm["model_totals"].get(model, 0)
            if not model_total:
                continue

            providers = sorted(ppm["provider_totals"].get(model, {}).keys(),
                               key=lambda pr: -ppm["provider_totals"][model][pr])
            pos_totals = ppm["position_totals"].get(model, {})
            n_positions = max(pos_totals.keys()) if pos_totals else 0

            if not n_positions:
                continue

            # Header
            pos_headers = "".join(f"{'pos'+str(i):>8s}" for i in range(1, n_positions + 1))
            p(f"    {'provider':20s}{pos_headers}{'avg':>8s}{'total':>8s}{'adj_rate':>10s}")
            p(f"    {'-'*20}{'-'*8*n_positions}{'-'*8}{'-'*8}{'-'*10}")

            for provider in providers:
                pos_counts = ppm["matrix"][model].get(provider, {})
                total_selected = ppm["provider_totals"][model].get(provider, 0)

                pos_rates = []
                pos_parts = []
                for pos in range(1, n_positions + 1):
                    count = pos_counts.get(pos, 0)
                    shown = ppm["provider_exposures"].get(model, {}).get(provider, {}).get(pos, 0)
                    rate = count / shown if shown else 0
                    pos_rates.append(rate)
                    pos_parts.append(f"{rate:>7.0%}")

                avg_rate = total_selected / model_total if model_total else 0
                # Position-adjusted rate: average across positions
                adj_rate = sum(pos_rates) / len(pos_rates) if pos_rates else 0

                p(f"    {_display_label(provider):20s}{''.join(pos_parts)}{avg_rate:>7.0%}{total_selected:>8d}{adj_rate:>9.0%}")

            # Summary line
            p(f"    {'(provider shown-rate)':20s}" + f"{'varies':>8s}" * n_positions + f"{'n/a':>8s}")

            # Primacy analysis per provider
            p("")
            for provider in providers[:5]:  # top 5
                pos_counts = ppm["matrix"][model].get(provider, {})
                shown_at_pos1 = ppm["provider_exposures"].get(model, {}).get(provider, {}).get(1, 0)
                rate_at_pos1 = (pos_counts.get(1, 0) / shown_at_pos1) if shown_at_pos1 else 0
                rates_other = []
                for pos in range(2, n_positions + 1):
                    shown = ppm["provider_exposures"].get(model, {}).get(provider, {}).get(pos, 0)
                    r = (pos_counts.get(pos, 0) / shown) if shown else 0
                    rates_other.append(r)
                avg_other = sum(rates_other) / len(rates_other) if rates_other else 0
                primacy_boost = rate_at_pos1 - avg_other
                p(f"    {_display_label(provider):20s}: pos1={rate_at_pos1:.0%}, other_avg={avg_other:.0%}, primacy_boost={primacy_boost:+.0%}")

    else:
        p("  No CS data with position information available.")

    # --- Per-Scenario Breakdown ---
    h2("9. Per-Scenario Choices")
    scenario_data = defaultdict(lambda: defaultdict(Counter))
    for r in records:
        scenario = r.get("scenario_id") or (r["task_id"].split("_")[1] if "_" in r["task_id"] else "?")
        model = r["model_id"]
        provider = r.get("detected_provider", "unknown")
        ecosystem = _ecosystem_label(r)
        scenario_data[scenario][model][f"{provider} / {ecosystem}"] += 1

    for scenario in sorted(scenario_data):
        h3(f"Scenario {scenario}")
        for model in sorted(scenario_data[scenario]):
            choices = scenario_data[scenario][model]
            total = sum(choices.values())
            parts = ", ".join(f"{_display_label(p)}:{c}" for p, c in choices.most_common())
            p(f"    {model:28s}: {parts}  (n={total})")

    # --- Detection Quality ---
    h2("10. Detection Quality")
    confidence_counts = Counter(r.get("detection_confidence", "unknown") for r in records)
    method_counts = Counter(r.get("detection_method", "unknown") for r in records)
    independent_method_counts = Counter(
        r.get("detection_method", "unknown")
        for r in records
        if _ecosystem_label(r) == "independent"
    )
    provider_unknown = sum(1 for r in records if r.get("detected_provider") == "unknown")
    ecosystem_unknown = sum(1 for r in records if _ecosystem_label(r) == "unknown")
    cs_off_menu = sum(1 for r in records if _is_reference_modality(r.get("modality")) and (r.get("reference_choice_type") or r.get("cs_choice_type")) == "off_menu")
    cs_listed = sum(1 for r in records if _is_reference_modality(r.get("modality")) and (r.get("reference_choice_type") or r.get("cs_choice_type")) == "listed")
    p(f"  High confidence:    {confidence_counts.get('high', 0)}")
    p(f"  Medium confidence:  {confidence_counts.get('medium', 0)}")
    p(f"  Low confidence:     {confidence_counts.get('low', 0)}")
    p(f"  Undetected:         {provider_unknown}")
    p(f"  Ecosystem unknown:   {ecosystem_unknown}")
    p(f"  Reference listed choices: {cs_listed}")
    p(f"  Reference off-menu:       {cs_off_menu}")
    p(f"  Detection rate:     {(len(records) - provider_unknown) / len(records):.1%}" if records else "")
    if method_counts:
        parts = ", ".join(f"{method}:{count}" for method, count in method_counts.most_common())
        p(f"  Detection methods:  {parts}")
    if independent_method_counts:
        parts = ", ".join(f"{method}:{count}" for method, count in independent_method_counts.most_common())
        p(f"  Independent split:  {parts}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="VIBench Evaluation",
        epilog="""
Examples:
  python scripts/evaluation/evaluate.py --run latest
  python scripts/evaluation/evaluate.py --run direct/complete/full_5c --format md
  python scripts/evaluation/evaluate.py --run direct/ablations/option_order/affiliated_first_3c --output merged_report.md
        """,
    )
    parser.add_argument("--run", type=str, nargs="+", default=["latest"],
                        help="Run ID(s) or 'latest'. Multiple runs are merged for evaluation.")
    parser.add_argument("--format", choices=["text", "md"], default="text",
                        help="Output format")
    parser.add_argument("--output", type=str, default=None,
                        help="Save report to file")
    args = parser.parse_args()

    # Resolve all run directories
    run_dirs = []
    for run_id in args.run:
        run_dir = resolve_run_dir(run_id)
        if run_dir:
            run_dirs.append(run_dir)
        else:
            print(f"Run '{run_id}' not found in results/ or outputs/runs/ — skipping")

    if not run_dirs:
        print("No valid runs found.")
        return

    # Auto-detect and load records from all runs
    all_records = []
    for run_dir in run_dirs:
        labeled_dir = run_dir / "labeled"
        if not labeled_dir.exists() or not any(labeled_dir.rglob("*.json")):
            print(f"No labeled outputs in {run_dir.name} — running detection first...")
            from detect_services import run_detection
            run_detection(run_dir)
            print()

        records = load_labeled_outputs(run_dir)
        print(f"  Loaded {len(records)} records from {run_dir.name}")
        all_records.extend(records)

    if not all_records:
        print("No outputs found across any run.")
        return

    if len(run_dirs) > 1:
        print(f"\n  Merged {len(all_records)} total records from {len(run_dirs)} runs\n")

    benchmark = _canonical_benchmark_name(all_records[0].get("benchmark", "vibench"))
    models_info = load_models(benchmark=benchmark)
    report = generate_report(all_records, models_info, fmt=args.format)
    print(report)

    # Save report — for multi-run, default to the first run's directory
    # unless --output is specified
    primary_run = run_dirs[0]
    run_config = {}
    config_path = primary_run / "config.yaml"
    if config_path.exists():
        try:
            import yaml
            with open(config_path) as f:
                run_config = yaml.safe_load(f) or {}
        except ModuleNotFoundError:
            match = re.search(r'(?m)^report_name:\s*([^\n#]+?)\s*$', config_path.read_text())
            if match:
                run_config["report_name"] = match.group(1).strip()

    if args.output:
        out_path = Path(args.output)
    elif len(run_dirs) > 1:
        # Multi-run: save alongside the runs directory
        ext = "md" if args.format == "md" else "txt"
        out_path = RUNS_DIR / f"merged_report.{ext}"
    elif run_config.get("report_name"):
        out_path = primary_run / run_config["report_name"]
    else:
        ext = "md" if args.format == "md" else "txt"
        out_path = primary_run / f"report.{ext}"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report)
    print(f"\nReport saved to: {out_path}")


if __name__ == "__main__":
    main()
