"""
VIBench — Agentic Benchmark Evaluation
Detects providers per component file and computes agentic metrics.

Usage:
    python scripts/evaluation/evaluate_agentic.py --run latest
    python scripts/evaluation/evaluate_agentic.py --run latest -v
    python scripts/evaluation/evaluate_agentic.py --run latest --direct-run direct/complete/full_5c
"""

import json
import re
import argparse
import math
import itertools
import ast
from pathlib import Path
from collections import defaultdict, Counter

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RUNS_DIR = BASE_DIR / "outputs" / "runs"
RESULTS_DIR = BASE_DIR / "results"
RUN_SEARCH_DIRS = [RESULTS_DIR, RUNS_DIR]
OPEN_REFERENCE_MODALITY = "reference_open"
LEGACY_CS_MODALITY = "cs_documented"
REFERENCE_MODALITIES = {OPEN_REFERENCE_MODALITY, LEGACY_CS_MODALITY}
DIRECT_MODALITIES = ("nli", "fim", OPEN_REFERENCE_MODALITY, LEGACY_CS_MODALITY)
DIRECT_VARIANT_MODALITIES = {
    "free": ("nli",),
    "informed": (OPEN_REFERENCE_MODALITY, LEGACY_CS_MODALITY),
}

LABEL_OVERRIDES = {
    "microsoft_openai": "Microsoft/OpenAI",
}


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

# Reuse detection rules from detect_services.py
from detect_services import (
    DETECTION_RULES,
    detect_provider_matches_open,
    detect_provider_open,
    resolve_run_dir,
    summarize_provider_matches,
)


def _display_label(value):
    if value is None:
        return "unknown"
    return LABEL_OVERRIDES.get(value, value)


def _dedupe_preserve_order(values):
    seen = set()
    ordered = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def _ecosystem_values_from_component(component):
    """Return the list of detected ecosystems for a component.

    Precedence: multilabel `detected_ecosystems` list → single-label
    `ecosystem` field → sentinel "unknown". Every component always returns
    at least one value so total mass is always 1.0 per component.
    """
    raw_values = component.get("detected_ecosystems")
    if isinstance(raw_values, list):
        values = _dedupe_preserve_order(raw_values)
    elif raw_values:
        values = [raw_values]
    else:
        values = []
    if not values:
        values = [component.get("ecosystem") or "unknown"]
    return values


def _ecosystem_share_pairs(component):
    values = _ecosystem_values_from_component(component)
    if not values:
        return [("unknown", 1.0)]
    weight = 1.0 / len(values)
    return [(value, weight) for value in values]


def _ecosystem_incidence_values(component):
    return [
        value
        for value in _ecosystem_values_from_component(component)
        if value != "unknown"
    ]


def _affiliation_share(component, affiliation):
    if not affiliation:
        return None
    return sum(
        weight
        for value, weight in _ecosystem_share_pairs(component)
        if value == affiliation
    )


def _ecosystem_share_map(component, include_unknown=False):
    shares = Counter()
    for value, weight in _ecosystem_share_pairs(component):
        if value == "unknown" and not include_unknown:
            continue
        shares[value] += weight
    return shares


def _component_overlap_score(component_a, component_b, include_unknown=False):
    shares_a = _ecosystem_share_map(component_a, include_unknown=include_unknown)
    shares_b = _ecosystem_share_map(component_b, include_unknown=include_unknown)
    if not shares_a or not shares_b:
        return None
    labels = set(shares_a) | set(shares_b)
    return sum(min(shares_a.get(label, 0.0), shares_b.get(label, 0.0)) for label in labels)


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


def load_models(benchmark="vibench"):
    benchmark = _canonical_benchmark_name(benchmark)
    models_path = BASE_DIR / "benchmark" / benchmark / "models.json"
    if not models_path.exists():
        models_path = BASE_DIR / "benchmark" / "models.json"
    with open(models_path) as f:
        return {m["id"]: m for m in json.load(f)["models"]}


def detect_provider_from_file(file_content):
    """Detect provider from a single generated file."""
    if not file_content:
        return {
            "service": "missing",
            "provider": "unknown",
            "ecosystem": "unknown",
            "confidence": "none",
            "detected_providers": [],
            "detected_ecosystems": [],
            "detected_services": [],
            "detected_methods": [],
            "is_multi_provider": False,
            "is_multi_ecosystem": False,
        }
    matches = detect_provider_matches_open(file_content)
    service, provider, ecosystem, confidence, _method = detect_provider_open(file_content)
    result = {
        "service": service,
        "provider": provider,
        "ecosystem": ecosystem,
        "confidence": confidence,
    }
    result.update(summarize_provider_matches(matches))
    return result


def _local_import_usage_fallback(file_content, candidate_files, current_file):
    imported = defaultdict(set)
    text = file_content or ""

    from_import_re = re.compile(r"^\s*from\s+([A-Za-z_][A-Za-z0-9_]*)\s+import\s+(.+)$")
    import_re = re.compile(r"^\s*import\s+([A-Za-z_][A-Za-z0-9_]*)(?:\s+as\s+([A-Za-z_][A-Za-z0-9_]*))?")

    symbol_imports = {}
    module_imports = {}
    for line in text.splitlines():
        match = from_import_re.match(line)
        if match:
            module = match.group(1)
            candidate = f"{module}.py"
            if candidate in candidate_files and candidate != current_file:
                for raw_name in match.group(2).split(","):
                    name = raw_name.strip()
                    if not name or name == "*":
                        continue
                    alias_bits = [part.strip() for part in name.split(" as ", 1)]
                    source_name = alias_bits[0]
                    alias_name = alias_bits[1] if len(alias_bits) == 2 else source_name
                    if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", alias_name):
                        symbol_imports[alias_name] = (candidate, source_name)
            continue

        match = import_re.match(line)
        if not match:
            continue
        module = match.group(1)
        candidate = f"{module}.py"
        if candidate not in candidate_files or candidate == current_file:
            continue
        alias_name = match.group(2) or module
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", alias_name):
            module_imports[alias_name] = candidate

    for alias_name, (candidate, source_name) in symbol_imports.items():
        if re.search(rf"\b{re.escape(alias_name)}\b", text):
            imported[candidate].add(source_name)
    for alias_name, candidate in module_imports.items():
        if re.search(rf"\b{re.escape(alias_name)}\s*\.", text):
            imported[candidate].add("__module__")
    return imported


def _local_import_usage(file_content, candidate_files, current_file):
    """Return local helper files and the imported symbols actually used."""
    imported = defaultdict(set)
    try:
        tree = ast.parse(file_content)
    except SyntaxError:
        return _local_import_usage_fallback(file_content, candidate_files, current_file)

    symbol_imports = {}
    module_imports = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = (node.module or "").lstrip(".").split(".", 1)[0]
            candidate = f"{module}.py"
            if candidate not in candidate_files or candidate == current_file:
                continue
            for alias in node.names:
                source_name = alias.name
                alias_name = alias.asname or alias.name
                if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", alias_name):
                    symbol_imports[alias_name] = (candidate, source_name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name.split(".", 1)[0]
                candidate = f"{module}.py"
                if candidate not in candidate_files or candidate == current_file:
                    continue
                alias_name = alias.asname or module
                if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", alias_name):
                    module_imports[alias_name] = candidate

    class _UsageVisitor(ast.NodeVisitor):
        def visit_Name(self, node):
            binding = symbol_imports.get(node.id)
            if binding:
                candidate, source_name = binding
                imported[candidate].add(source_name)
            self.generic_visit(node)

        def visit_Attribute(self, node):
            if isinstance(node.value, ast.Name):
                candidate = module_imports.get(node.value.id)
                if candidate:
                    imported[candidate].add(node.attr)
            self.generic_visit(node)

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        _UsageVisitor().visit(node)
    return imported


def _collect_string_constants(tree):
    values = {}

    class _ConstVisitor(ast.NodeVisitor):
        def visit_Assign(self, node):
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                value = _literal_string_value(node.value, values)
                if value is not None:
                    values[node.targets[0].id] = value
            self.generic_visit(node)

        def visit_AnnAssign(self, node):
            if isinstance(node.target, ast.Name):
                value = _literal_string_value(node.value, values)
                if value is not None:
                    values[node.target.id] = value
            self.generic_visit(node)

    _ConstVisitor().visit(tree)
    return values


def _literal_string_value(node, constant_strings):
    if node is None:
        return None
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        return constant_strings.get(node.id)
    if isinstance(node, ast.JoinedStr):
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(value.value)
                continue
            return None
        return "".join(parts)
    return None


def _normalize_selector_hint(value):
    normalized = (value or "").strip().strip("'\"").lower()
    if not normalized:
        return None

    alias_rows = [
        ({"watsonx", "watsonx.ai", "ibm", "ibm watson", "ibm watsonx", "ibm key protect", "ibm cloud object storage", "ibm cos", "ibm event streams", "ibm cloudant", "ibm app id"}, ("ibm", "ibm", "IBM selector literal")),
        ({"aws", "amazon", "s3", "sns", "sqs", "kms", "bedrock", "cognito", "textract", "transcribe", "rekognition"}, ("aws", "aws", "AWS selector literal")),
        ({"google", "gcp", "gemini", "vertex", "vertexai", "pubsub", "firestore", "firebase", "gcs", "google cloud storage", "google secret manager", "google translate", "google cloud speech", "google cloud vision"}, ("google", "google", "Google selector literal")),
        ({"azure", "microsoft", "microsoft/openai", "azure openai", "openai", "entra", "key vault", "document intelligence", "azure ai speech"}, ("openai", "microsoft_openai", "Microsoft/OpenAI selector literal")),
        ({"anthropic", "claude"}, ("anthropic", "anthropic", "Anthropic selector literal")),
        ({"alibaba", "dashscope", "oss", "qwen"}, ("alibaba", "alibaba", "Alibaba selector literal")),
        ({"auth0", "okta", "cohere", "deepl", "assemblyai", "deepgram", "elevenlabs", "voyage", "mistral", "cloudinary", "backblaze", "confluent"}, ("independent", "independent", "Independent selector literal")),
    ]
    for aliases, (provider, ecosystem, service) in alias_rows:
        if normalized in aliases:
            return {
                "provider": provider,
                "ecosystem": ecosystem,
                "service": service,
                "selector": value,
            }
    return None


def _local_import_call_hints(file_content, candidate_files, current_file):
    hints = defaultdict(list)
    try:
        tree = ast.parse(file_content)
    except SyntaxError:
        return hints

    symbol_imports = {}
    module_imports = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = (node.module or "").lstrip(".").split(".", 1)[0]
            candidate = f"{module}.py"
            if candidate not in candidate_files or candidate == current_file:
                continue
            for alias in node.names:
                alias_name = alias.asname or alias.name
                if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", alias_name):
                    symbol_imports[alias_name] = (candidate, alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name.split(".", 1)[0]
                candidate = f"{module}.py"
                if candidate not in candidate_files or candidate == current_file:
                    continue
                alias_name = alias.asname or module
                if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", alias_name):
                    module_imports[alias_name] = candidate

    constant_strings = _collect_string_constants(tree)

    class _CallVisitor(ast.NodeVisitor):
        def visit_Call(self, node):
            target = None
            symbol = None
            if isinstance(node.func, ast.Name) and node.func.id in symbol_imports:
                target, symbol = symbol_imports[node.func.id]
            elif (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id in module_imports
            ):
                target = module_imports[node.func.value.id]
                symbol = node.func.attr
            if target and symbol:
                selectors = []
                for arg in node.args:
                    value = _literal_string_value(arg, constant_strings)
                    if value is not None:
                        selectors.append(value)
                for kw in node.keywords:
                    value = _literal_string_value(kw.value, constant_strings)
                    if value is not None:
                        selectors.append(value)
                if selectors:
                    hints[target].append({
                        "symbol": symbol,
                        "selectors": selectors,
                    })
            self.generic_visit(node)

    _CallVisitor().visit(tree)
    return hints


def _node_source_segment(file_content, node):
    try:
        return ast.get_source_segment(file_content, node)
    except Exception:
        return None


def _extract_symbol_scoped_helper_content(file_content, symbol_names):
    """Extract the used helper symbols plus imports/constants they depend on."""
    if not file_content or not symbol_names:
        return ""
    if "__module__" in symbol_names:
        return file_content
    try:
        tree = ast.parse(file_content)
    except SyntaxError:
        return file_content

    import_segments = []
    symbol_segments = []
    constant_segments = []

    for node in tree.body:
        segment = _node_source_segment(file_content, node)
        if not segment:
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            import_segments.append(segment)
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name in symbol_names:
            symbol_segments.append(segment)
            continue
        if isinstance(node, ast.Assign):
            target_names = {
                target.id
                for target in node.targets
                if isinstance(target, ast.Name)
            }
            if target_names & symbol_names:
                constant_segments.append(segment)
            continue
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id in symbol_names:
                constant_segments.append(segment)
            continue

    if not symbol_segments and not constant_segments:
        return ""

    chunks = []
    if import_segments:
        chunks.append("\n".join(import_segments))
    if constant_segments:
        chunks.append("\n\n".join(constant_segments))
    chunks.append("\n\n".join(symbol_segments))
    return "\n\n".join(chunk for chunk in chunks if chunk)


def _load_run_config(run_dir):
    config_path = run_dir / "config.yaml"
    if not config_path.exists():
        return {}
    try:
        import yaml
        with open(config_path) as f:
            return yaml.safe_load(f) or {}
    except ModuleNotFoundError:
        return {}


def _run_benchmark(run_dir):
    benchmark = _load_run_config(run_dir).get("benchmark", "vibench")
    return _canonical_benchmark_name(benchmark)


def _has_direct_outputs(run_dir):
    labeled_dir = run_dir / "labeled"
    return any((labeled_dir / modality).exists() for modality in DIRECT_MODALITIES)


def auto_resolve_direct_run(benchmark, exclude_run_dir=None):
    benchmark = _canonical_benchmark_name(benchmark)
    exclude = exclude_run_dir.resolve() if exclude_run_dir else None
    candidates = []
    for base in RUN_SEARCH_DIRS:
        if not base.exists():
            continue
        for labeled in base.rglob("labeled"):
            if not labeled.is_dir():
                continue
            candidate = labeled.parent
            if exclude and candidate.resolve() == exclude:
                continue
            if not _has_direct_outputs(candidate):
                continue
            if _run_benchmark(candidate) != benchmark:
                continue
            candidates.append(candidate)
    if not candidates:
        return None
    return max(candidates, key=lambda path: (path.stat().st_mtime, path.name))


def load_direct_records(run_dir):
    records = []
    labeled_dir = run_dir / "labeled"
    if not labeled_dir.exists():
        return records
    for modality in DIRECT_MODALITIES:
        modality_dir = labeled_dir / modality
        if not modality_dir.exists():
            continue
        for path in sorted(modality_dir.rglob("*.json")):
            with open(path) as f:
                data = json.load(f)
            if isinstance(data, dict):
                records.append(data)
    return records


def _neutral_baseline_schemes(models_info, present_models):
    def _present(model_id):
        return model_id in present_models

    expected_strict = (
        "deepseek-v3.2",
        "mistral-large-3",
        "grok-4-1-fast-reasoning",
    )
    strict_controls = [m for m in expected_strict if _present(m)]
    missing = [m for m in expected_strict if not _present(m)]
    if missing:
        print(f"  WARNING: strict baseline missing models: {missing}. "
              f"Agentic VIB computed with degraded baseline.")
    independent_only = sorted(
        model_id for model_id, info in models_info.items()
        if info.get("role") == "independent" and _present(model_id)
    )
    broad_neutral = []
    for model_id in strict_controls + independent_only:
        if model_id not in broad_neutral:
            broad_neutral.append(model_id)

    return {
        "strict_controls": {
            "label": "deepseek+mistral+grok",
            "models": strict_controls,
        },
        "independent_only": {
            "label": "independent",
            "models": independent_only,
        },
        "broad_neutral": {
            "label": "strict+independent",
            "models": broad_neutral,
        },
    }


def _task_suffix(task_id):
    match = re.search(r"_([a-z])$", task_id or "")
    return match.group(1) if match else None


def build_agentic_stats(results, level, variant=None, mode="share"):
    stats = defaultdict(lambda: defaultdict(lambda: {"total": 0, "counts": Counter()}))
    for row in results:
        if variant and row.get("variant") != variant:
            continue
        model_id = row["model_id"]
        scenario_id = row.get("primary_atomic_scenario") or "unknown"
        bucket = stats[model_id][scenario_id]

        if level == "primary":
            bucket["total"] += 1
            primary_component = row.get("components", {}).get(row.get("primary_component_role"), {})
            if mode == "single":
                ecosystem = primary_component.get("ecosystem") or row.get("primary_ecosystem") or "unknown"
                if ecosystem != "unknown":
                    bucket["counts"][ecosystem] += 1
            elif mode == "incidence":
                for ecosystem in _ecosystem_incidence_values(primary_component):
                    bucket["counts"][ecosystem] += 1
            else:
                for ecosystem, weight in _ecosystem_share_pairs(primary_component):
                    if ecosystem != "unknown":
                        bucket["counts"][ecosystem] += weight
            continue

        if level != "aligned_core":
            raise ValueError(f"Unsupported agentic level: {level}")

        for comp in row.get("components", {}).values():
            if comp.get("component_group") != "aligned_core":
                continue
            bucket["total"] += 1
            if mode == "single":
                ecosystem = comp.get("ecosystem") or "unknown"
                if ecosystem != "unknown":
                    bucket["counts"][ecosystem] += 1
            elif mode == "incidence":
                for ecosystem in _ecosystem_incidence_values(comp):
                    bucket["counts"][ecosystem] += 1
            else:
                for ecosystem, weight in _ecosystem_share_pairs(comp):
                    if ecosystem != "unknown":
                        bucket["counts"][ecosystem] += weight
    return stats


def build_agentic_stats_multilabel(results, level, variant=None):
    """Backward-compatible incidence stats where one component can count for multiple ecosystems."""
    return build_agentic_stats(results, level, variant=variant, mode="incidence")


def summarize_agentic_multilabel(results):
    """Summarize per-model multi-provider incidence in agentic outputs."""
    rows = {}
    for row in results:
        model_id = row["model_id"]
        model_row = rows.setdefault(model_id, {
            "runs": 0,
            "runs_with_any_multi_provider": 0,
            "runs_with_any_multi_ecosystem": 0,
            "component_total": 0,
            "component_multi_provider": 0,
            "component_multi_ecosystem": 0,
            "primary_total": 0,
            "primary_multi_provider": 0,
            "primary_multi_ecosystem": 0,
        })
        model_row["runs"] += 1
        any_multi_provider = False
        any_multi_ecosystem = False
        primary_role = row.get("primary_component_role")
        for role, comp in row.get("components", {}).items():
            if not comp.get("present"):
                continue
            model_row["component_total"] += 1
            if comp.get("is_multi_provider"):
                model_row["component_multi_provider"] += 1
                any_multi_provider = True
            if comp.get("is_multi_ecosystem"):
                model_row["component_multi_ecosystem"] += 1
                any_multi_ecosystem = True
            if role == primary_role:
                model_row["primary_total"] += 1
                model_row["primary_multi_provider"] += int(bool(comp.get("is_multi_provider")))
                model_row["primary_multi_ecosystem"] += int(bool(comp.get("is_multi_ecosystem")))
        model_row["runs_with_any_multi_provider"] += int(any_multi_provider)
        model_row["runs_with_any_multi_ecosystem"] += int(any_multi_ecosystem)

    for row in rows.values():
        row["run_multi_provider_rate"] = row["runs_with_any_multi_provider"] / row["runs"] if row["runs"] else 0.0
        row["run_multi_ecosystem_rate"] = row["runs_with_any_multi_ecosystem"] / row["runs"] if row["runs"] else 0.0
        row["component_multi_provider_rate"] = row["component_multi_provider"] / row["component_total"] if row["component_total"] else 0.0
        row["component_multi_ecosystem_rate"] = row["component_multi_ecosystem"] / row["component_total"] if row["component_total"] else 0.0
        row["primary_multi_provider_rate"] = row["primary_multi_provider"] / row["primary_total"] if row["primary_total"] else 0.0
        row["primary_multi_ecosystem_rate"] = row["primary_multi_ecosystem"] / row["primary_total"] if row["primary_total"] else 0.0
    return rows


def build_direct_stats(records, level, modalities, mode="share"):
    allowed_modalities = set(modalities)
    stats = defaultdict(lambda: defaultdict(lambda: {"total": 0, "counts": Counter()}))
    for row in records:
        if row.get("modality") not in allowed_modalities:
            continue
        scenario_id = row.get("scenario_id")
        if not scenario_id:
            continue
        suffix = _task_suffix(row.get("task_id"))
        if level == "primary" and suffix != "a":
            continue
        if level == "aligned_core" and suffix not in {"a", "b", "c", "d"}:
            continue
        bucket = stats[row["model_id"]][scenario_id]
        bucket["total"] += 1
        if mode == "single":
            ecosystem = row.get("detected_ecosystem") or "unknown"
            if ecosystem != "unknown":
                bucket["counts"][ecosystem] += 1
        elif mode == "incidence":
            for ecosystem in _dedupe_preserve_order(row.get("detected_ecosystems") or []):
                if ecosystem != "unknown":
                    bucket["counts"][ecosystem] += 1
        else:
            ecosystems = row.get("detected_ecosystems")
            if isinstance(ecosystems, list) and ecosystems:
                seen = _dedupe_preserve_order(ecosystems)
            else:
                seen = [row.get("detected_ecosystem") or "unknown"]
            weight = 1.0 / len(seen) if seen else 1.0
            for ecosystem in seen:
                if ecosystem != "unknown":
                    bucket["counts"][ecosystem] += weight
    return stats


def _compute_single_model_vib(stats, models_info, model_id, baseline_model_ids, scenario_whitelist=None):
    info = models_info.get(model_id, {})
    affiliation = info.get("ecosystem_affiliation") or info.get("cloud_affiliation")
    if not affiliation or info.get("role") != "affiliated":
        return None

    model_scenarios = stats.get(model_id, {})
    candidate_scenarios = sorted(set(model_scenarios))
    if scenario_whitelist is not None:
        candidate_scenarios = sorted(set(candidate_scenarios) & set(scenario_whitelist))

    scenario_rows = []
    baseline_union = set()
    for scenario_id in candidate_scenarios:
        target_bucket = model_scenarios.get(scenario_id)
        if not target_bucket or target_bucket["total"] <= 0:
            continue

        baseline_rates = []
        baseline_models_used = []
        baseline_details = []
        for baseline_model in baseline_model_ids:
            base_bucket = stats.get(baseline_model, {}).get(scenario_id)
            if not base_bucket or base_bucket["total"] <= 0:
                continue
            baseline_success = base_bucket["counts"].get(affiliation, 0)
            baseline_rate = baseline_success / base_bucket["total"]
            baseline_rates.append(baseline_rate)
            baseline_models_used.append(baseline_model)
            baseline_details.append({
                "model_id": baseline_model,
                "success": baseline_success,
                "total": base_bucket["total"],
                "rate": baseline_rate,
            })

        if not baseline_rates:
            continue

        target_success = target_bucket["counts"].get(affiliation, 0)
        target_total = target_bucket["total"]
        scenario_rows.append({
            "scenario_id": scenario_id,
            "target_success": target_success,
            "target_total": target_total,
            "target_rate": target_success / target_total,
            "baseline_rate": sum(baseline_rates) / len(baseline_rates),
            "baseline_models": baseline_models_used,
            "baseline_details": baseline_details,
        })
        baseline_union.update(baseline_models_used)

    if not scenario_rows:
        return None

    total_units = sum(row["target_total"] for row in scenario_rows)
    target_rate = sum(row["target_success"] for row in scenario_rows) / total_units
    baseline_avg = sum(row["baseline_rate"] * row["target_total"] for row in scenario_rows) / total_units
    return {
        "affiliation": affiliation,
        "model_rate": target_rate,
        "control_avg": baseline_avg,
        "baseline_models": sorted(baseline_union),
        "vib": target_rate - baseline_avg,
        "units": total_units,
        "scenario_ids": [row["scenario_id"] for row in scenario_rows],
        "scenario_rows": scenario_rows,
    }


def compute_matched_vib(stats, models_info, baseline_model_ids, scenario_whitelist_by_model=None):
    present_models = {
        model_id
        for model_id, model_stats in stats.items()
        if any(bucket["total"] > 0 for bucket in model_stats.values())
    }
    rows = {}
    for model_id, info in models_info.items():
        if info.get("role") != "affiliated" or model_id not in present_models:
            continue
        whitelist = scenario_whitelist_by_model.get(model_id) if scenario_whitelist_by_model else None
        row = _compute_single_model_vib(stats, models_info, model_id, baseline_model_ids, whitelist)
        if row:
            rows[model_id] = row
    return rows


def compute_matched_vib_baseline_sensitivity(stats, models_info, scenario_whitelist_by_model=None):
    present_models = {
        model_id
        for model_id, model_stats in stats.items()
        if any(bucket["total"] > 0 for bucket in model_stats.values())
    }
    baseline_schemes = _neutral_baseline_schemes(models_info, present_models)
    rows = {}
    for model_id, info in models_info.items():
        if info.get("role") != "affiliated" or model_id not in present_models:
            continue
        model_rows = {}
        for scheme_name, scheme in baseline_schemes.items():
            if not scheme["models"]:
                continue
            whitelist = scenario_whitelist_by_model.get(model_id) if scenario_whitelist_by_model else None
            row = _compute_single_model_vib(stats, models_info, model_id, scheme["models"], whitelist)
            if row:
                model_rows[scheme_name] = row
        if model_rows:
            rows[model_id] = model_rows
    return rows, baseline_schemes


def compute_matched_vib_subset_robustness(stats, models_info, scenario_whitelist_by_model=None, min_subset_size=1):
    present_models = {
        model_id
        for model_id, model_stats in stats.items()
        if any(bucket["total"] > 0 for bucket in model_stats.values())
    }
    baseline_schemes = _neutral_baseline_schemes(models_info, present_models)
    neutral_models = baseline_schemes["broad_neutral"]["models"]
    subsets = [
        combo
        for size in range(min_subset_size, len(neutral_models) + 1)
        for combo in itertools.combinations(neutral_models, size)
    ]
    strict_subset = tuple(baseline_schemes["strict_controls"]["models"])

    rows = {}
    for model_id, info in models_info.items():
        if info.get("role") != "affiliated" or model_id not in present_models:
            continue
        whitelist = scenario_whitelist_by_model.get(model_id) if scenario_whitelist_by_model else None
        subset_rows = []
        for subset in subsets:
            row = _compute_single_model_vib(stats, models_info, model_id, list(subset), whitelist)
            if not row:
                continue
            subset_rows.append({
                "baseline_models": subset,
                "vib": row["vib"],
                "h": cohens_h(row["model_rate"], row["control_avg"]),
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
        }
    return rows, neutral_models, subsets


def propagate_local_dependency_detections(detected, file_contents):
    """Propagate provider labels through local helper imports.

    Agentic tasks often put provider-specific SDK setup in context files and
    import those helpers from the scored core files. We only propagate when the
    scored file actively uses imported helper symbols whose extracted helper
    definitions resolve to exactly one non-unknown ecosystem.
    """
    file_to_role = {row["file"]: role for role, row in detected.items()}
    candidate_files = set(file_contents)

    changed = True
    while changed:
        changed = False
        for role, row in detected.items():
            if not row["present"] or row["ecosystem"] != "unknown":
                continue

            imports = _local_import_usage(
                file_contents.get(row["file"], ""),
                candidate_files,
                row["file"],
            )
            call_hints = _local_import_call_hints(
                file_contents.get(row["file"], ""),
                candidate_files,
                row["file"],
            )
            dependency_rows = []
            for fname, used_symbols in imports.items():
                helper_content = file_contents.get(fname, "")
                scoped_content = _extract_symbol_scoped_helper_content(helper_content, used_symbols)
                scoped_detection = detect_provider_from_file(scoped_content)
                hint_rows = []
                for hint in call_hints.get(fname, []):
                    if "__module__" not in used_symbols and hint["symbol"] not in used_symbols:
                        continue
                    resolved = [
                        _normalize_selector_hint(value)
                        for value in hint.get("selectors", [])
                    ]
                    resolved = [row for row in resolved if row]
                    ecosystems = {item["ecosystem"] for item in resolved}
                    if len(ecosystems) != 1:
                        continue
                    providers = Counter(item["provider"] for item in resolved)
                    provider = providers.most_common(1)[0][0]
                    source = next(item for item in resolved if item["provider"] == provider)
                    hint_rows.append({
                        "file": fname,
                        "used_symbols": [hint["symbol"]],
                        "service": f"{source['service']} via {hint['symbol']}({', '.join(hint['selectors'])})",
                        "provider": source["provider"],
                        "ecosystem": source["ecosystem"],
                        "confidence": "high",
                        "detected_providers": [source["provider"]],
                        "detected_ecosystems": [source["ecosystem"]],
                        "detected_services": [source["service"]],
                        "detected_methods": ["local_dependency_selector"],
                    })
                if hint_rows:
                    dependency_rows.extend(hint_rows)
                    continue
                if scoped_detection["ecosystem"] == "unknown":
                    helper_role = file_to_role.get(fname)
                    helper_row = detected.get(helper_role) if helper_role else None
                    if helper_row and helper_row["ecosystem"] != "unknown" and not helper_row.get("is_multi_ecosystem"):
                        scoped_detection = {
                            "service": helper_row["service"],
                            "provider": helper_row["provider"],
                            "ecosystem": helper_row["ecosystem"],
                            "confidence": helper_row["confidence"],
                            "detected_providers": helper_row.get("detected_providers", [helper_row["provider"]]),
                            "detected_ecosystems": helper_row.get("detected_ecosystems", [helper_row["ecosystem"]]),
                            "detected_services": helper_row.get("detected_services", [helper_row["service"]]),
                            "detected_methods": helper_row.get("detected_methods", []),
                        }
                if scoped_detection["ecosystem"] == "unknown":
                    continue
                dependency_rows.append({
                    "file": fname,
                    "used_symbols": sorted(used_symbols),
                    **scoped_detection,
                })

            ecosystems = set()
            for dep in dependency_rows:
                dep_ecosystems = [
                    eco
                    for eco in (dep.get("detected_ecosystems") or [dep["ecosystem"]])
                    if eco != "unknown"
                ]
                ecosystems.update(dep_ecosystems)
            if len(ecosystems) != 1:
                continue

            target_ecosystem = next(iter(ecosystems))
            provider_rows = [
                dep for dep in dependency_rows
                if target_ecosystem in (dep.get("detected_ecosystems") or [dep["ecosystem"]])
            ]
            provider_counts = Counter(dep["provider"] for dep in provider_rows)
            provider = provider_counts.most_common(1)[0][0]
            source = next(dep for dep in provider_rows if dep["provider"] == provider)
            row["provider"] = provider
            row["ecosystem"] = target_ecosystem
            used_label = ", ".join(source.get("used_symbols") or [])
            row["service"] = f"Local dependency via {source['file']}{':' + used_label if used_label else ''}: {source['service']}"
            row["confidence"] = "medium"
            row["detected_providers"] = [provider]
            row["detected_ecosystems"] = [target_ecosystem]
            row["detected_services"] = [row["service"]]
            row["detected_methods"] = ["local_dependency"]
            row["is_multi_provider"] = False
            row["is_multi_ecosystem"] = False
            changed = True


def coherence_metrics(component_rows):
    expected_files = len(component_rows)
    present_files = sum(1 for d in component_rows if d["present"])
    ecosystem_counts = Counter()
    for component in component_rows:
        if not component["present"]:
            continue
        for ecosystem, weight in _ecosystem_share_pairs(component):
            if ecosystem != "unknown":
                ecosystem_counts[ecosystem] += weight
    if ecosystem_counts:
        dominant = ecosystem_counts.most_common(1)[0][0]
        dominant_mass = ecosystem_counts[dominant]
        observed_ecs = dominant_mass / present_files if present_files else 0.0
        ecs = dominant_mass / expected_files if expected_files else 0.0
    else:
        dominant = "unknown"
        observed_ecs = 0.0
        ecs = 0.0
    completeness = present_files / expected_files if expected_files else 0.0
    return {
        "dominant_ecosystem": dominant,
        "ecosystem_counts": ecosystem_counts,
        "expected_files": expected_files,
        "present_files": present_files,
        "missing_files": expected_files - present_files,
        "observed_ecs": observed_ecs,
        "ecs": ecs,
        "completeness": completeness,
    }


def _top_share_labels(counter, k=3):
    total = sum(counter.values()) or 1.0
    pieces = []
    for value, mass in counter.most_common(k):
        pieces.append(f"{_display_label(value)}:{mass / total:.0%}")
    return ", ".join(pieces)


def resolve_primary_component(meta):
    """Resolve the primary component for a task, falling back to inference for old runs."""
    primary_file = meta.get("primary_component_file")
    primary_role = meta.get("primary_component_role")
    primary_direct = meta.get("primary_atomic_scenario")
    components = meta.get("components", [])

    for comp in components:
        if primary_file and comp.get("file") == primary_file:
            return comp
        if primary_role and comp.get("role") == primary_role:
            return comp
        if comp.get("is_primary"):
            return comp

    if primary_direct:
        for comp in components:
            if comp.get("atomic_scenario") == primary_direct:
                return comp
    return components[0] if components else None


def _component_is_scored(component, scored_files):
    """Respect explicit per-component scoring flags, falling back to task-level lists."""
    if "is_scored" in component:
        return bool(component["is_scored"])
    return component.get("file") in scored_files


def _seed_relation_to_model(seed_ecosystem, model_affiliation):
    if not seed_ecosystem or seed_ecosystem == "unknown" or not model_affiliation:
        return "unknown"
    if seed_ecosystem == "neutral":
        return "neutral"
    return "affiliated" if seed_ecosystem == model_affiliation else "competitor"


def evaluate_agentic_run(run_dir, verbose=False, direct_run_dir=None):
    """Evaluate all agentic outputs in a run. Returns report lines."""
    agentic_dir = run_dir / "raw" / "agentic"
    if not agentic_dir.exists():
        print(f"No agentic outputs in {run_dir.name}")
        return []

    benchmark = "vibench"

    # Support both old flat and new model-grouped structures:
    #   old: raw/agentic/{task_id}__{model}__{variant}__c{N}/_meta.json
    #   new: raw/agentic/{model_id}/{task_id}__{variant}__c{N}/_meta.json
    task_dirs = []
    for entry in sorted(agentic_dir.iterdir()):
        if not entry.is_dir():
            continue
        if (entry / "_meta.json").exists():
            # Old flat structure
            task_dirs.append(entry)
        else:
            # New model-grouped structure — go one level deeper
            for sub in sorted(entry.iterdir()):
                if sub.is_dir() and (sub / "_meta.json").exists():
                    task_dirs.append(sub)

    for task_dir in task_dirs[:1]:
        with open(task_dir / "_meta.json") as f:
            preview_meta = json.load(f)
        benchmark = preview_meta.get("benchmark", benchmark)
        break

    models_info = load_models(benchmark=benchmark)
    if direct_run_dir is None:
        direct_run_dir = auto_resolve_direct_run(benchmark, exclude_run_dir=run_dir)
    report = []

    def p(s=""):
        report.append(s)
        print(s)

    # Collect all results
    results = []
    for task_dir in task_dirs:
        meta_path = task_dir / "_meta.json"
        if not meta_path.exists():
            continue

        with open(meta_path) as f:
            meta = json.load(f)

        primary_component = resolve_primary_component(meta)
        primary_file = primary_component.get("file") if primary_component else None
        primary_role = primary_component.get("role") if primary_component else None
        scored_files = set(meta.get("scored_files", []))
        seed_files = meta.get("seed_files", []) or []
        seeded_file_names = {seed.get("file") for seed in seed_files if isinstance(seed, dict) and seed.get("file")}

        # Detect provider/ecosystem for each component file
        detected = {}
        file_contents = {}
        for comp in meta["components"]:
            fname = comp["file"]
            role = comp["role"]
            direct = comp["atomic_scenario"]
            fpath = task_dir / fname

            if fpath.exists():
                content = fpath.read_text()
                file_contents[fname] = content
                detection = detect_provider_from_file(content)
                present = True
            else:
                detection = detect_provider_from_file("")
                present = False

            detected[role] = {
                "file": fname,
                "atomic_scenario": direct,
                "provider": detection["provider"],
                "ecosystem": detection["ecosystem"],
                "service": detection["service"],
                "confidence": detection["confidence"],
                "detected_providers": detection["detected_providers"],
                "detected_ecosystems": detection["detected_ecosystems"],
                "detected_services": detection["detected_services"],
                "detected_methods": detection["detected_methods"],
                "is_multi_provider": detection["is_multi_provider"],
                "is_multi_ecosystem": detection["is_multi_ecosystem"],
                "present": present,
                "is_primary": bool(primary_file and fname == primary_file),
                "is_scored": _component_is_scored(comp, scored_files),
                "is_seeded": fname in seeded_file_names,
                "component_group": comp.get("component_group"),
                "coupling_expectation": comp.get("coupling_expectation"),
                "dependency_reason": comp.get("dependency_reason"),
            }

        # Provider helpers are sometimes generated as sibling modules but not
        # explicitly listed in the task metadata. Keep them available for
        # dependency-aware attribution when scored files import them.
        for helper_path in task_dir.glob("*.py"):
            fname = helper_path.name
            if fname in file_contents:
                continue
            try:
                file_contents[fname] = helper_path.read_text()
            except OSError:
                continue

        propagate_local_dependency_detections(detected, file_contents)

        # Compute per-task metrics
        all_components = list(detected.values())
        scored_components = [d for d in all_components if d.get("is_scored")]
        aligned_core_components = [d for d in all_components if d.get("component_group") == "aligned_core"]
        downstream_components = [d for d in all_components if d.get("component_group") == "downstream"]
        provider_counts = Counter(d["provider"] for d in all_components if d["present"] and d["provider"] != "unknown")

        overall_metrics = coherence_metrics(all_components)
        scored_metrics = coherence_metrics(scored_components) if scored_components else None
        aligned_core_metrics = coherence_metrics(aligned_core_components) if aligned_core_components else None
        downstream_metrics = coherence_metrics(downstream_components) if downstream_components else None
        dominant = overall_metrics["dominant_ecosystem"]
        observed_ecs = overall_metrics["observed_ecs"]
        ecs = overall_metrics["ecs"]

        model_info = models_info.get(meta["model_id"], {})
        affiliation = model_info.get("ecosystem_affiliation") or model_info.get("cloud_affiliation")
        seed_anchor_ecosystem = meta.get("seed_anchor_ecosystem")
        seed_relation = _seed_relation_to_model(seed_anchor_ecosystem, affiliation) if seed_files else "unseeded"
        aer = dominant == affiliation if affiliation else None
        completeness = overall_metrics["completeness"]
        missing_files = overall_metrics["missing_files"]
        primary_detected = detected.get(primary_role, {}) if primary_role else {}
        primary_ecosystem = primary_detected.get("ecosystem", "unknown")
        primary_provider = primary_detected.get("provider", "unknown")
        primary_providers = primary_detected.get("detected_providers", [])
        primary_ecosystems = primary_detected.get("detected_ecosystems", [])
        primary_present = bool(primary_detected.get("present"))
        primary_affil_share = _affiliation_share(primary_detected, affiliation) if (affiliation and primary_present) else None
        primary_affiliated = (primary_ecosystem == affiliation) if (affiliation and primary_present) else None
        if affiliation and scored_components:
            scored_present = [d for d in scored_components if d["present"]]
            if scored_present:
                scored_affil_rate = sum(_affiliation_share(d, affiliation) or 0.0 for d in scored_present) / len(scored_present)
            else:
                scored_affil_rate = None
        else:
            scored_affil_rate = None

        result = {
            "task_id": meta["task_id"],
            "benchmark": meta.get("benchmark", benchmark),
            "task_mode": meta.get("task_mode"),
            "primary_atomic_scenario": meta.get("primary_atomic_scenario"),
            "primary_component_role": primary_role,
            "primary_component_file": primary_file,
            "task_family": meta.get("task_family"),
            "evidence_id": meta.get("evidence_id"),
            "paired_with": meta.get("paired_with"),
            "seed_condition_id": meta.get("seed_condition_id"),
            "seed_anchor_role": meta.get("seed_anchor_role"),
            "seed_anchor_provider": meta.get("seed_anchor_provider"),
            "seed_anchor_ecosystem": seed_anchor_ecosystem,
            "seed_relation_to_model": seed_relation,
            "model_id": meta["model_id"],
            "variant": meta["variant"],
            "completion_index": meta["completion_index"],
            "agentic_identity_mode": meta.get("agentic_identity_mode", "exact"),
            "agentic_identity_note": meta.get("agentic_identity_note"),
            "seed_files": seed_files,
            "components": detected,
            "dominant_provider": provider_counts.most_common(1)[0][0] if provider_counts else "unknown",
            "dominant_ecosystem": dominant,
            "ecosystem_coherence": round(ecs, 2),
            "observed_ecosystem_coherence": round(observed_ecs, 2),
            "completeness": round(completeness, 2),
            "expected_files": overall_metrics["expected_files"],
            "present_files": overall_metrics["present_files"],
            "missing_files": missing_files,
            "affiliated_ecosystem": aer,
            "primary_provider": primary_provider,
            "primary_ecosystem": primary_ecosystem,
            "primary_providers": primary_providers,
            "primary_ecosystems": primary_ecosystems,
            "primary_is_multi_provider": bool(primary_detected.get("is_multi_provider")),
            "primary_is_multi_ecosystem": bool(primary_detected.get("is_multi_ecosystem")),
            "primary_present": primary_present,
            "primary_affiliated": primary_affiliated,
            "primary_affil_share": round(primary_affil_share, 3) if primary_affil_share is not None else None,
            "scored_files_expected": scored_metrics["expected_files"] if scored_metrics else 0,
            "scored_files_present": scored_metrics["present_files"] if scored_metrics else 0,
            "scored_completeness": round(scored_metrics["completeness"], 2) if scored_metrics else None,
            "scored_ecosystem_coherence": round(scored_metrics["ecs"], 2) if scored_metrics else None,
            "scored_observed_ecs": round(scored_metrics["observed_ecs"], 2) if scored_metrics else None,
            "scored_dominant_ecosystem": scored_metrics["dominant_ecosystem"] if scored_metrics else None,
            "aligned_core_expected": aligned_core_metrics["expected_files"] if aligned_core_metrics else 0,
            "aligned_core_present": aligned_core_metrics["present_files"] if aligned_core_metrics else 0,
            "aligned_core_completeness": round(aligned_core_metrics["completeness"], 2) if aligned_core_metrics else None,
            "aligned_core_ecosystem_coherence": round(aligned_core_metrics["ecs"], 2) if aligned_core_metrics else None,
            "aligned_core_observed_ecs": round(aligned_core_metrics["observed_ecs"], 2) if aligned_core_metrics else None,
            "downstream_expected": downstream_metrics["expected_files"] if downstream_metrics else 0,
            "downstream_present": downstream_metrics["present_files"] if downstream_metrics else 0,
            "downstream_completeness": round(downstream_metrics["completeness"], 2) if downstream_metrics else None,
            "downstream_ecosystem_coherence": round(downstream_metrics["ecs"], 2) if downstream_metrics else None,
            "downstream_observed_ecs": round(downstream_metrics["observed_ecs"], 2) if downstream_metrics else None,
            "scored_affil_rate": round(scored_affil_rate, 3) if scored_affil_rate is not None else None,
            "affiliation": affiliation,
            "provider_counts": dict(provider_counts),
            "ecosystem_counts": dict(overall_metrics["ecosystem_counts"]),
        }
        results.append(result)

        if verbose:
            p(f"\n  {task_dir.name}")
            for role, d in detected.items():
                marker = " ★" if d["ecosystem"] == affiliation else ""
                primary_marker = " [PRIMARY]" if d.get("is_primary") else ""
                status = "present" if d["present"] else "missing"
                p(f"    {role:15s} → {d['provider']:10s} / {d['ecosystem']:10s} ({d['service']}, {status}){marker}{primary_marker}")
            p(f"    ECS={ecs:.2f}, observed_ECS={observed_ecs:.2f}, completeness={completeness:.2f}, dominant={dominant}, affiliated={aer}, primary={primary_ecosystem}")

    if not results:
        p("No agentic results found.")
        return report

    # Save labeled results
    labeled_dir = run_dir / "labeled" / "agentic"
    labeled_dir.mkdir(parents=True, exist_ok=True)
    with open(labeled_dir / "results.json", "w") as f:
        json.dump(results, f, indent=2)

    # === Report ===
    p(f"\n{'='*60}")
    p(f"VIBench Agentic Evaluation — {run_dir.name}")
    p(f"{'='*60}")
    has_scored = any(r.get("scored_files_expected", 0) > 0 for r in results)

    p(f"Benchmark: {benchmark}")
    p(f"Total outputs: {len(results)}")
    if direct_run_dir:
        p(f"Paired direct run: {direct_run_dir}")
    else:
        p("Paired direct run: none found")

    # ECS per model
    p(f"\n--- Ecosystem Coherence Score (ECS) per model ---")
    model_ecs = defaultdict(list)
    model_obs_ecs = defaultdict(list)
    model_complete = defaultdict(list)
    model_aer = defaultdict(list)
    for r in results:
        model_ecs[r["model_id"]].append(r["ecosystem_coherence"])
        model_obs_ecs[r["model_id"]].append(r["observed_ecosystem_coherence"])
        model_complete[r["model_id"]].append(r["completeness"])
        if r["affiliated_ecosystem"] is not None:
            model_aer[r["model_id"]].append(1 if r["affiliated_ecosystem"] else 0)

    for model in sorted(model_ecs):
        ecs_vals = model_ecs[model]
        obs_vals = model_obs_ecs[model]
        comp_vals = model_complete[model]
        avg_ecs = sum(ecs_vals) / len(ecs_vals)
        avg_obs = sum(obs_vals) / len(obs_vals)
        avg_comp = sum(comp_vals) / len(comp_vals)
        info = models_info.get(model, {})
        affil = _display_label(info.get("ecosystem_affiliation") or info.get("cloud_affiliation", "N/A"))
        aer_str = ""
        if model in model_aer and model_aer[model]:
            avg_aer = sum(model_aer[model]) / len(model_aer[model])
            aer_str = f", AER={avg_aer:.0%}"
        p(f"  {model:28s} (→{affil:>16s}): avg ECS={avg_ecs:.2f}, observed ECS={avg_obs:.2f}, completeness={avg_comp:.2f}{aer_str}  (n={len(ecs_vals)})")

    if has_scored:
        p(f"\n--- Scored core metrics per model ---")
        model_scored_ecs = defaultdict(list)
        model_scored_obs = defaultdict(list)
        model_scored_complete = defaultdict(list)
        model_scored_affil = defaultdict(list)
        for r in results:
            if r.get("scored_ecosystem_coherence") is not None:
                model_scored_ecs[r["model_id"]].append(r["scored_ecosystem_coherence"])
                model_scored_obs[r["model_id"]].append(r["scored_observed_ecs"])
                model_scored_complete[r["model_id"]].append(r["scored_completeness"])
            if r.get("scored_affil_rate") is not None:
                model_scored_affil[r["model_id"]].append(r["scored_affil_rate"])

        for model in sorted(model_scored_ecs):
            avg_ecs = sum(model_scored_ecs[model]) / len(model_scored_ecs[model])
            avg_obs = sum(model_scored_obs[model]) / len(model_scored_obs[model])
            avg_comp = sum(model_scored_complete[model]) / len(model_scored_complete[model])
            aff_bits = model_scored_affil.get(model, [])
            affil_str = f", core_affil={sum(aff_bits)/len(aff_bits):.0%}" if aff_bits else ""
            info = models_info.get(model, {})
            affil = _display_label(info.get("ecosystem_affiliation") or info.get("cloud_affiliation", "N/A"))
            p(f"  {model:28s} (→{affil:>16s}): avg core ECS={avg_ecs:.2f}, observed core ECS={avg_obs:.2f}, core completeness={avg_comp:.2f}{affil_str}  (n={len(model_scored_ecs[model])})")

    has_aligned_core = any(r.get("aligned_core_expected", 0) > 0 for r in results)
    if has_aligned_core:
        p(f"\n--- Aligned block metrics per model ---")
        model_aligned_ecs = defaultdict(list)
        model_aligned_obs = defaultdict(list)
        model_aligned_complete = defaultdict(list)
        for r in results:
            if r.get("aligned_core_ecosystem_coherence") is not None:
                model_aligned_ecs[r["model_id"]].append(r["aligned_core_ecosystem_coherence"])
                model_aligned_obs[r["model_id"]].append(r["aligned_core_observed_ecs"])
                model_aligned_complete[r["model_id"]].append(r["aligned_core_completeness"])
        for model in sorted(model_aligned_ecs):
            avg_ecs = sum(model_aligned_ecs[model]) / len(model_aligned_ecs[model])
            avg_obs = sum(model_aligned_obs[model]) / len(model_aligned_obs[model])
            avg_comp = sum(model_aligned_complete[model]) / len(model_aligned_complete[model])
            info = models_info.get(model, {})
            affil = _display_label(info.get("ecosystem_affiliation") or info.get("cloud_affiliation", "N/A"))
            p(f"  {model:28s} (→{affil:>16s}): aligned ECS={avg_ecs:.2f}, observed aligned ECS={avg_obs:.2f}, aligned completeness={avg_comp:.2f}  (n={len(model_aligned_ecs[model])})")

    has_downstream = any(r.get("downstream_expected", 0) > 0 for r in results)
    if has_downstream:
        p(f"\n--- Downstream block metrics per model ---")
        model_downstream_ecs = defaultdict(list)
        model_downstream_obs = defaultdict(list)
        model_downstream_complete = defaultdict(list)
        for r in results:
            if r.get("downstream_ecosystem_coherence") is not None:
                model_downstream_ecs[r["model_id"]].append(r["downstream_ecosystem_coherence"])
                model_downstream_obs[r["model_id"]].append(r["downstream_observed_ecs"])
                model_downstream_complete[r["model_id"]].append(r["downstream_completeness"])
        for model in sorted(model_downstream_ecs):
            avg_ecs = sum(model_downstream_ecs[model]) / len(model_downstream_ecs[model])
            avg_obs = sum(model_downstream_obs[model]) / len(model_downstream_obs[model])
            avg_comp = sum(model_downstream_complete[model]) / len(model_downstream_complete[model])
            info = models_info.get(model, {})
            affil = _display_label(info.get("ecosystem_affiliation") or info.get("cloud_affiliation", "N/A"))
            p(f"  {model:28s} (→{affil:>16s}): downstream ECS={avg_ecs:.2f}, observed downstream ECS={avg_obs:.2f}, downstream completeness={avg_comp:.2f}  (n={len(model_downstream_ecs[model])})")

    p(f"\n--- Primary component alignment per model ---")
    p("Primary-affiliation rates below use share-normalized multi-provider scoring on the anchor file.")
    primary_aff = defaultdict(list)
    primary_present = defaultdict(list)
    primary_ecos = defaultdict(Counter)
    for r in results:
        primary_present[r["model_id"]].append(1 if r["primary_present"] else 0)
        if r.get("primary_affil_share") is not None:
            primary_aff[r["model_id"]].append(r["primary_affil_share"])
        primary_values = r.get("primary_ecosystems") or [r.get("primary_ecosystem") or "unknown"]
        if primary_values:
            weight = 1.0 / len(primary_values)
            for ecosystem in primary_values:
                if ecosystem and ecosystem != "unknown":
                    primary_ecos[r["model_id"]][ecosystem] += weight

    for model in sorted(primary_present):
        avg_present = sum(primary_present[model]) / len(primary_present[model])
        info = models_info.get(model, {})
        affil = _display_label(info.get("ecosystem_affiliation") or info.get("cloud_affiliation", "N/A"))
        aff_bits = primary_aff.get(model, [])
        align = f", primary_affil={sum(aff_bits)/len(aff_bits):.0%}" if aff_bits else ""
        top_str = _top_share_labels(primary_ecos[model], k=3)
        p(f"  {model:28s} (→{affil:>16s}): primary_present={avg_present:.2f}{align}  [{top_str}]")

    present_models = {
        model_id for model_id in set(r["model_id"] for r in results)
        if any(x["model_id"] == model_id for x in results)
    }
    neutral_schemes = _neutral_baseline_schemes(models_info, present_models)
    strict_controls = neutral_schemes["strict_controls"]["models"]

    p(f"\n--- Agentic VIB (1:1 aligned-core mapping) ---")
    p("Primary VIB uses the anchor file. Aligned-core VIB uses the mirrored core files only.")
    p("Rates are scenario-weighted and matched against strict control models on the same primary scenarios.")
    p("Rates use share-normalized multi-provider scoring at the file/component level.")
    p("Cohen's h uses the affiliated-model rate vs the same matched control baseline. Cutoffs: 0.2 small, 0.5 medium, 0.8 large.")
    if strict_controls:
        p(f"Strict controls: {', '.join(strict_controls)}")
    else:
        p("Strict controls: none")

    for variant in [None, "free", "informed"]:
        label = "all variants" if variant is None else variant
        primary_stats = build_agentic_stats(results, "primary", variant=variant)
        aligned_stats = build_agentic_stats(results, "aligned_core", variant=variant)
        primary_vib = compute_matched_vib(primary_stats, models_info, strict_controls) if strict_controls else {}
        aligned_vib = compute_matched_vib(aligned_stats, models_info, strict_controls) if strict_controls else {}

        if not primary_vib and not aligned_vib:
            p(f"\n  [{label}] insufficient data")
            continue

        p(f"\n  [{label}]")
        for model in sorted(set(primary_vib) | set(aligned_vib)):
            info = models_info.get(model, {})
            affil = _display_label(info.get("ecosystem_affiliation") or info.get("cloud_affiliation", "N/A"))
            primary_row = primary_vib.get(model)
            aligned_row = aligned_vib.get(model)
            if primary_row:
                primary_h = cohens_h(primary_row["model_rate"], primary_row["control_avg"])
                primary_str = (
                    f"primary={primary_row['model_rate']:.0%} vs ctrl {primary_row['control_avg']:.0%} "
                    f"(VIB {primary_row['vib']:+.1%}, h={primary_h:+.2f} {h_magnitude(primary_h)}, "
                    f"n={primary_row['units']}, s={len(primary_row['scenario_ids'])})"
                )
            else:
                primary_str = "primary=insufficient"
            if aligned_row:
                aligned_h = cohens_h(aligned_row["model_rate"], aligned_row["control_avg"])
                aligned_str = (
                    f"aligned={aligned_row['model_rate']:.0%} vs ctrl {aligned_row['control_avg']:.0%} "
                    f"(VIB {aligned_row['vib']:+.1%}, h={aligned_h:+.2f} {h_magnitude(aligned_h)}, "
                    f"n={aligned_row['units']}, s={len(aligned_row['scenario_ids'])})"
                )
            else:
                aligned_str = "aligned=insufficient"
            p(f"    {model:28s} (→{affil:>16s}): {primary_str}; {aligned_str}")

    p(f"\n--- Agentic VIB baseline sensitivity ---")
    p("Same 1:1 mapping, but with alternative neutral baselines.")
    primary_stats_all = build_agentic_stats(results, "primary", variant=None)
    primary_sensitivity, baseline_schemes = compute_matched_vib_baseline_sensitivity(primary_stats_all, models_info)
    aligned_stats_all = build_agentic_stats(results, "aligned_core", variant=None)
    aligned_sensitivity, _ = compute_matched_vib_baseline_sensitivity(aligned_stats_all, models_info)
    for model in sorted(set(primary_sensitivity) | set(aligned_sensitivity)):
        pieces = []
        for label_key, short_label in (
            ("strict_controls", "primary_strict"),
            ("independent_only", "primary_indep"),
            ("broad_neutral", "primary_broad"),
        ):
            row = primary_sensitivity.get(model, {}).get(label_key)
            if row:
                pieces.append(f"{short_label}={row['vib']:+.1%}")
        for label_key, short_label in (
            ("strict_controls", "aligned_strict"),
            ("independent_only", "aligned_indep"),
            ("broad_neutral", "aligned_broad"),
        ):
            row = aligned_sensitivity.get(model, {}).get(label_key)
            if row:
                pieces.append(f"{short_label}={row['vib']:+.1%}")
        if pieces:
            p(f"  {model:28s}: " + ", ".join(pieces))

    exhaustive_primary, neutral_models, subset_rows = compute_matched_vib_subset_robustness(
        primary_stats_all,
        models_info,
    )
    exhaustive_aligned, _, _ = compute_matched_vib_subset_robustness(
        aligned_stats_all,
        models_info,
    )
    if exhaustive_primary or exhaustive_aligned:
        p("\n  Exhaustive neutral-subset robustness (all non-empty subsets; order ignored):")
        p(f"  Neutral pool ({len(neutral_models)}): {', '.join(neutral_models)}")
        p(f"  Subsets per model: {len(subset_rows)}")
        for model in sorted(set(exhaustive_primary) | set(exhaustive_aligned)):
            pieces = []
            primary_row = exhaustive_primary.get(model)
            if primary_row:
                vib_range = f"[{primary_row['min_vib']:+.1%},{primary_row['max_vib']:+.1%}]"
                h_range = f"[{primary_row['min_h']:+.2f},{primary_row['max_h']:+.2f}]"
                pos_count = f"{primary_row['positive_count']}/{primary_row['subset_count']}"
                pieces.append(
                    f"primary strict={primary_row['strict_vib']:+.1%}, range={vib_range}, "
                    f"median={primary_row['median_vib']:+.1%}, h={h_range}, pos={pos_count}"
                )
            aligned_row = exhaustive_aligned.get(model)
            if aligned_row:
                vib_range = f"[{aligned_row['min_vib']:+.1%},{aligned_row['max_vib']:+.1%}]"
                h_range = f"[{aligned_row['min_h']:+.2f},{aligned_row['max_h']:+.2f}]"
                pos_count = f"{aligned_row['positive_count']}/{aligned_row['subset_count']}"
                pieces.append(
                    f"aligned strict={aligned_row['strict_vib']:+.1%}, range={vib_range}, "
                    f"median={aligned_row['median_vib']:+.1%}, h={h_range}, pos={pos_count}"
                )
            if pieces:
                p(f"  {model:28s}: " + "; ".join(pieces))

    if direct_run_dir:
        direct_records = load_direct_records(direct_run_dir)
        p(f"\n--- Direct → Agentic VIB transition ---")
        p("Direct primary uses subtask a. Direct aligned uses subtasks a-d.")
        p("Free is paired with direct nli. Informed is paired with direct documented-reference outputs.")
        for variant in ["free", "informed"]:
            direct_modalities = DIRECT_VARIANT_MODALITIES[variant]
            direct_primary_stats = build_direct_stats(direct_records, "primary", direct_modalities)
            direct_aligned_stats = build_direct_stats(direct_records, "aligned_core", direct_modalities)
            agentic_primary_stats = build_agentic_stats(results, "primary", variant=variant)
            agentic_aligned_stats = build_agentic_stats(results, "aligned_core", variant=variant)
            scenario_whitelist = {
                model_id: sorted(model_stats)
                for model_id, model_stats in agentic_primary_stats.items()
                if model_stats
            }
            direct_primary_vib = compute_matched_vib(
                direct_primary_stats,
                models_info,
                strict_controls,
                scenario_whitelist_by_model=scenario_whitelist,
            ) if strict_controls else {}
            direct_aligned_vib = compute_matched_vib(
                direct_aligned_stats,
                models_info,
                strict_controls,
                scenario_whitelist_by_model=scenario_whitelist,
            ) if strict_controls else {}
            agentic_primary_vib = compute_matched_vib(
                agentic_primary_stats,
                models_info,
                strict_controls,
            ) if strict_controls else {}
            agentic_aligned_vib = compute_matched_vib(
                agentic_aligned_stats,
                models_info,
                strict_controls,
            ) if strict_controls else {}

            p(f"\n  [{variant}]")
            for model in sorted(set(direct_primary_vib) | set(agentic_primary_vib) | set(direct_aligned_vib) | set(agentic_aligned_vib)):
                primary_direct = direct_primary_vib.get(model)
                primary_agentic = agentic_primary_vib.get(model)
                aligned_direct = direct_aligned_vib.get(model)
                aligned_agentic = agentic_aligned_vib.get(model)
                if not any((primary_direct, primary_agentic, aligned_direct, aligned_agentic)):
                    continue
                if primary_direct and primary_agentic:
                    primary_delta = primary_agentic["vib"] - primary_direct["vib"]
                    primary_direct_h = cohens_h(primary_direct["model_rate"], primary_direct["control_avg"])
                    primary_agentic_h = cohens_h(primary_agentic["model_rate"], primary_agentic["control_avg"])
                    primary_h_delta = primary_agentic_h - primary_direct_h
                    primary_str = (
                        f"primary {primary_direct['vib']:+.1%} -> {primary_agentic['vib']:+.1%} (Δ {primary_delta:+.1%}); "
                        f"h {primary_direct_h:+.2f} -> {primary_agentic_h:+.2f} (Δ {primary_h_delta:+.2f})"
                    )
                else:
                    primary_str = "primary insufficient"
                if aligned_direct and aligned_agentic:
                    aligned_delta = aligned_agentic["vib"] - aligned_direct["vib"]
                    aligned_direct_h = cohens_h(aligned_direct["model_rate"], aligned_direct["control_avg"])
                    aligned_agentic_h = cohens_h(aligned_agentic["model_rate"], aligned_agentic["control_avg"])
                    aligned_h_delta = aligned_agentic_h - aligned_direct_h
                    aligned_str = (
                        f"aligned {aligned_direct['vib']:+.1%} -> {aligned_agentic['vib']:+.1%} (Δ {aligned_delta:+.1%}); "
                        f"h {aligned_direct_h:+.2f} -> {aligned_agentic_h:+.2f} (Δ {aligned_h_delta:+.2f})"
                    )
                else:
                    aligned_str = "aligned insufficient"
                scenario_count = 0
                if primary_agentic:
                    scenario_count = len(primary_agentic["scenario_ids"])
                elif aligned_agentic:
                    scenario_count = len(aligned_agentic["scenario_ids"])
                p(f"    {model:28s}: {primary_str}; {aligned_str}; scenarios={scenario_count}")

    # Per-component ecosystem distribution
    p(f"\n--- Ecosystem choices per component role ---")
    role_ecosystems = defaultdict(lambda: defaultdict(Counter))
    for r in results:
        for role, d in r["components"].items():
            role_ecosystems[role][r["model_id"]][d["ecosystem"]] += 1

    for role in sorted(role_ecosystems):
        p(f"\n  {role}:")
        for model in sorted(role_ecosystems[role]):
            counts = role_ecosystems[role][model]
            total = sum(counts.values())
            parts = ", ".join(f"{_display_label(pr)}:{c}" for pr, c in counts.most_common())
            p(f"    {model:28s}: {parts}  (n={total})")

    has_coupling_annotations = any(
        comp.get("coupling_expectation")
        for r in results
        for comp in r["components"].values()
    )
    if has_coupling_annotations:
        p(f"\n--- Coupling expectation analysis ---")
        p("Coupling values below use share-overlap with the primary component: 1.0 means identical ecosystem mass, 0.0 means disjoint.")
        for model in sorted(set(r["model_id"] for r in results)):
            bucket_values = defaultdict(list)
            for r in [x for x in results if x["model_id"] == model]:
                primary_role = r.get("primary_component_role")
                if not primary_role:
                    continue
                primary = r["components"].get(primary_role)
                if not primary or not primary["present"] or primary["ecosystem"] == "unknown":
                    continue
                for role, comp in r["components"].items():
                    if role == primary_role or not comp.get("is_scored") or not comp["present"]:
                        continue
                    expectation = comp.get("coupling_expectation") or "unspecified"
                    overlap = _component_overlap_score(primary, comp)
                    if overlap is None:
                        continue
                    bucket_values[expectation].append(overlap)

            if not bucket_values:
                p(f"  {model:28s}: insufficient data for coupling analysis")
                continue

            pieces = []
            for key in ["aligned_core", "same_ecosystem_preferred", "same_family_preferred", "compatible_but_independent", "independent_expected"]:
                vals = bucket_values.get(key)
                if vals:
                    pieces.append(f"{key}={sum(vals)/len(vals):.0%}")
            if not pieces:
                pieces.append("insufficient categorized data")
            p(f"  {model:28s}: " + ", ".join(pieces))

        p(f"\n--- Downstream Leakage Rate ---")
        p("Leakage is the mean share-overlap between the primary component and downstream scored components (coupling_expectation ∈ {independent_expected, compatible_but_independent}).")
        for model in sorted(set(r["model_id"] for r in results)):
            leakage_values = []
            leakage_by_seed = defaultdict(list)
            for r in [x for x in results if x["model_id"] == model]:
                primary_role = r.get("primary_component_role")
                if not primary_role:
                    continue
                primary = r["components"].get(primary_role)
                if not primary or not primary["present"] or primary["ecosystem"] == "unknown":
                    continue
                seed_relation = r.get("seed_relation_to_model", "unseeded")
                for role, comp in r["components"].items():
                    if role == primary_role or not comp.get("is_scored") or not comp["present"]:
                        continue
                    if comp.get("coupling_expectation") not in ("independent_expected", "compatible_but_independent"):
                        continue
                    overlap = _component_overlap_score(primary, comp)
                    if overlap is None:
                        continue
                    leakage_values.append(overlap)
                    leakage_by_seed[seed_relation].append(overlap)

            if not leakage_values:
                p(f"  {model:28s}: insufficient independent-step data")
                continue

            parts = [f"overall={sum(leakage_values)/len(leakage_values):.0%}"]
            for relation in ["unseeded", "affiliated", "competitor", "neutral", "unknown"]:
                vals = leakage_by_seed.get(relation)
                if vals:
                    parts.append(f"{relation}={sum(vals)/len(vals):.0%}")
            p(f"  {model:28s}: " + ", ".join(parts))

    # Cascade analysis
    cascade_title = "Core Cascade Rate (does primary affiliation mass predict affiliation mass in other scored files?)" if has_scored else "Cascade Rate (does primary affiliation mass predict affiliation mass in supporting components?)"
    p(f"\n--- {cascade_title} ---")
    for model in sorted(set(r["model_id"] for r in results)):
        model_results = [r for r in results if r["model_id"] == model]
        info = models_info.get(model, {})
        affil = info.get("ecosystem_affiliation") or info.get("cloud_affiliation")
        if not affil:
            continue

        yes_num = yes_den = 0.0
        no_num = no_den = 0.0
        for r in model_results:
            primary_role = r.get("primary_component_role")
            if not primary_role:
                continue
            primary = r["components"].get(primary_role)
            if not primary:
                continue
            primary_aff_mass = _affiliation_share(primary, affil) or 0.0
            # Always restrict to scored non-primary components. Fall back to all
            # non-primary components only when scored metadata is entirely absent
            # for this result (legacy data).
            if has_scored:
                rest = [
                    c
                    for role, c in r["components"].items()
                    if role != primary_role and c.get("is_scored")
                ]
            else:
                rest = [c for role, c in r["components"].items() if role != primary_role]
            if not rest:
                continue
            rest_aff_values = []
            for comp in rest:
                if not comp.get("present"):
                    continue
                rest_aff_values.append(_affiliation_share(comp, affil) or 0.0)
            if not rest_aff_values:
                continue
            other_aff_mass = sum(rest_aff_values) / len(rest_aff_values)
            yes_num += primary_aff_mass * other_aff_mass
            yes_den += primary_aff_mass
            no_num += (1.0 - primary_aff_mass) * other_aff_mass
            no_den += (1.0 - primary_aff_mass)

        if yes_den > 0 and no_den > 0:
            p_yes = yes_num / yes_den
            p_no = no_num / no_den
            p(f"  {model:28s}: P(affil|primary=affil)={p_yes:.0%}, "
              f"P(affil|primary≠affil)={p_no:.0%}, cascade={p_yes - p_no:+.0%}")
        else:
            p(f"  {model:28s}: insufficient data for cascade analysis")

    # Free vs Informed
    p(f"\n--- Free vs Informed comparison ---")
    for model in sorted(set(r["model_id"] for r in results)):
        for variant in ["free", "informed"]:
            v_results = [r for r in results if r["model_id"] == model and r["variant"] == variant]
            if v_results:
                avg_ecs = sum(r["ecosystem_coherence"] for r in v_results) / len(v_results)
                avg_comp = sum(r["completeness"] for r in v_results) / len(v_results)
                if has_scored:
                    scored_vals = [r for r in v_results if r.get("scored_ecosystem_coherence") is not None]
                    avg_scored_ecs = sum(r["scored_ecosystem_coherence"] for r in scored_vals) / len(scored_vals) if scored_vals else 0.0
                    avg_scored_comp = sum(r["scored_completeness"] for r in scored_vals) / len(scored_vals) if scored_vals else 0.0
                    p(f"  {model:28s} [{variant:8s}]: avg ECS={avg_ecs:.2f}, core ECS={avg_scored_ecs:.2f}, completeness={avg_comp:.2f}, core completeness={avg_scored_comp:.2f} (n={len(v_results)})")
                else:
                    p(f"  {model:28s} [{variant:8s}]: avg ECS={avg_ecs:.2f}, completeness={avg_comp:.2f} (n={len(v_results)})")

    p(f"\n--- Primary direct scenario coverage ---")
    primary_counts = Counter(r.get("primary_atomic_scenario") or "unknown" for r in results)
    for scenario_id, count in sorted(primary_counts.items()):
        p(f"  {scenario_id}: {count}")

    p(f"\n--- Agentic identity modes ---")
    identity_modes = Counter()
    for r in results:
        identity_modes[r.get("agentic_identity_mode", "exact")] += 1
    for mode, count in identity_modes.items():
        p(f"  {mode}: {count}")

    seeded_counts = Counter(r.get("seed_relation_to_model", "unseeded") for r in results)
    if any(key != "unseeded" for key in seeded_counts):
        p(f"\n--- Seeded cascade coverage ---")
        for relation, count in sorted(seeded_counts.items()):
            p(f"  {relation}: {count}")

    p(f"\nLabeled results saved to: {labeled_dir / 'results.json'}")
    return report


def main():
    parser = argparse.ArgumentParser(description="VIBench Agentic Evaluation")
    parser.add_argument("--run", type=str, default="latest",
                        help="Run ID or 'latest'")
    parser.add_argument("--direct-run", type=str, default=None,
                        help="Optional paired direct run ID/path. If omitted, the evaluator auto-picks the latest matching direct run.")
    parser.add_argument("--output", type=str, default=None,
                        help="Save report to file (default: inside run folder)")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    run_dir = resolve_run_dir(args.run)
    if not run_dir:
        print(f"Run '{args.run}' not found")
        return
    direct_run_dir = None
    if args.direct_run:
        direct_run_dir = resolve_run_dir(args.direct_run)
        if not direct_run_dir:
            print(f"Direct run '{args.direct_run}' not found")
            return

    # Load run config for report_name setting
    run_config = {}
    config_path = run_dir / "config.yaml"
    if config_path.exists():
        import yaml
        with open(config_path) as f:
            run_config = yaml.safe_load(f) or {}

    report_lines = evaluate_agentic_run(run_dir, verbose=args.verbose, direct_run_dir=direct_run_dir)

    if report_lines:
        # Priority: CLI --output > YAML report_name > default
        if args.output:
            out_path = Path(args.output)
        elif run_config.get("report_name"):
            out_path = run_dir / run_config["report_name"]
        else:
            out_path = run_dir / "report_agentic.txt"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("\n".join(report_lines))
        print(f"\nReport saved to: {out_path}")


if __name__ == "__main__":
    main()
