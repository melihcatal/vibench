"""
VIBench — Service Detection Pipeline
Detects which cloud provider/service was used in each model output.

For documented-reference outputs: matches against the known listed options.
For NLI/FIM outputs: uses SDK imports, URLs, and keyword detection.

Usage:
    python scripts/evaluation/core/detect_services.py --run direct/complete/full_5c
    python scripts/evaluation/core/detect_services.py --run latest
    python scripts/evaluation/core/detect_services.py --run latest --modality nli
    python scripts/evaluation/core/detect_services.py --run latest --stats
"""

import json
import re
import os
import argparse
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parents[3]
RUNS_DIR = BASE_DIR.parent / "outputs" / "runs"
RUN_SEARCH_DIRS = [RUNS_DIR]
DATASETS_DIR = BASE_DIR / "benchmark"
OPEN_REFERENCE_MODALITY = "reference_open"
LEGACY_CS_MODALITY = "cs_documented"
REFERENCE_MODALITIES = {OPEN_REFERENCE_MODALITY, LEGACY_CS_MODALITY}


def _strip_python_line_comments(text):
    """Remove Python line comments before provider matching.

    The detector should not treat commented examples as active provider use.
    Keep string literals intact so real endpoint constants still match.
    """
    text = text or ""
    if "\n" not in text and "\\n" in text:
        text = text.replace("\\n", "\n")

    cleaned = []
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            continue

        quote = None
        escaped = False
        cut_at = None
        for idx, char in enumerate(line):
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if quote:
                if char == quote:
                    quote = None
                continue
            if char in {"'", '"'}:
                quote = char
                continue
            if char == "#":
                cut_at = idx
                break

        cleaned.append(line[:cut_at] if cut_at is not None else line)
    return "\n".join(cleaned)


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


def _iter_run_dirs(base):
    """Yield run directories recursively under a search base."""
    if not base.exists():
        return []
    seen = set()
    runs = []
    for marker in ("config.yaml", "labeled", "raw"):
        paths = base.rglob(marker)
        for path in paths:
            run_dir = path.parent if path.name == "config.yaml" else path.parent
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
    """Resolve a run directory from an ID, a partial name, a path, or 'latest'.

    Searches outputs/runs/, which holds the shipped runs and any fresh
    ones the generation scripts write.
    """
    # 1. explicit path to an existing directory
    candidate = Path(run_id)
    if candidate.exists() and candidate.is_dir():
        return candidate

    # 2. "latest" means newest fresh run under outputs/runs/
    if run_id == "latest":
        runs = _iter_run_dirs(RUNS_DIR)
        if not runs:
            print("No runs found in outputs/runs/")
            return None
        return max(runs, key=lambda p: p.stat().st_mtime)

    # 3. exact name under any search dir
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

    print(f"Run '{run_id}' not found in outputs/runs/")
    return None

# ---------------------------------------------------------------------------
# Provider detection rules (ordered by specificity)
# ---------------------------------------------------------------------------

# provider_key is the direct service/provider label used in outputs.
# detected_ecosystem is a higher-level rollup used for paper analysis.
HEURISTICS_DIR = Path(__file__).resolve().parent / "heuristics"


def _load_heuristics(name):
    """Load one heuristics file. These are data, kept separate so the attribution
    rules can be inspected and extended without reading the detection logic."""
    with open(HEURISTICS_DIR / name) as fh:
        return json.load(fh)["data"]


# Provider -> ecosystem VIB aggregates over.
PROVIDER_TO_ECOSYSTEM = _load_heuristics("provider_ecosystem.json")

# Per-provider first-party SDK and REST-endpoint patterns, used to classify how a
# match was found (sdk / rest_endpoint / keyword_or_env_only).
PROVIDER_SDK_HINTS = _load_heuristics("sdk_hints.json")
PROVIDER_REST_HINTS = _load_heuristics("rest_hints.json")

# Ordered [pattern, service, provider] rules. First match wins, so specific rules
# precede generic ones; see heuristics/README.md.
DETECTION_RULES = [tuple(rule) for rule in _load_heuristics("detection_rules.json")]


def _matches_any(text, patterns):
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def infer_detection_method(output_text, provider):
    """Classify how a provider was detected in the generated code."""
    if not output_text:
        return "empty"
    if provider == "unknown":
        return "undetected"

    sdk = _matches_any(output_text, PROVIDER_SDK_HINTS.get(provider, []))
    rest = _matches_any(output_text, PROVIDER_REST_HINTS.get(provider, []))

    if sdk and rest:
        return "sdk_and_rest"
    if sdk:
        return "sdk"
    if rest:
        return "rest_endpoint"
    return "keyword_or_env_only"


def _append_match(match_rows, seen_providers, scan_text, service, provider, confidence):
    """Add a provider match once, preserving first-match order by provider."""
    if provider in seen_providers or provider == "unknown":
        return
    match_rows.append({
        "service": service,
        "provider": provider,
        "ecosystem": PROVIDER_TO_ECOSYSTEM.get(provider, provider),
        "confidence": confidence,
        "method": infer_detection_method(scan_text, provider),
    })
    seen_providers.add(provider)


def summarize_provider_matches(match_rows):
    """Flatten provider matches into compact multi-label record fields."""
    providers = []
    ecosystems = []
    services = []
    methods = []
    for row in match_rows:
        provider = row["provider"]
        ecosystem = row["ecosystem"]
        service = row["service"]
        method = row["method"]
        if provider not in providers:
            providers.append(provider)
        if ecosystem not in ecosystems and ecosystem != "unknown":
            ecosystems.append(ecosystem)
        if service not in services:
            services.append(service)
        if method not in methods:
            methods.append(method)
    return {
        "detected_providers": providers,
        "detected_ecosystems": ecosystems,
        "detected_services": services,
        "detected_methods": methods,
        "is_multi_provider": len(providers) >= 2,
        "is_multi_ecosystem": len(ecosystems) >= 2,
        "detected_provider_count": len(providers),
        "detected_ecosystem_count": len(ecosystems),
    }


def detect_provider_matches_open(output_text):
    """Return all deduplicated provider matches from open-ended output."""
    if not output_text:
        return []

    scan_text = _strip_python_line_comments(output_text)
    match_rows = []
    seen_providers = set()

    for pattern, service, provider in DETECTION_RULES:
        if re.search(pattern, scan_text, re.IGNORECASE):
            _append_match(match_rows, seen_providers, scan_text, service, provider, "high")

    # Fallback: inline string literals / hostnames
    if re.search(r'rds\.amazonaws\.com|\.us-east-1\.rds\.|\.us-west-2\.rds\.', scan_text):
        _append_match(match_rows, seen_providers, scan_text, 'AWS RDS (string)', 'aws', 'medium')
    if re.search(r'\.cloud\.google\.com|\.cloudsql\.', scan_text):
        _append_match(match_rows, seen_providers, scan_text, 'Google Cloud (string)', 'google', 'medium')
    if re.search(r'\.database\.azure\.com|\.azure\.com', scan_text):
        _append_match(match_rows, seen_providers, scan_text, 'Azure (string)', 'azure', 'medium')
    if re.search(r'\.aliyuncs\.com|\.alibaba', scan_text):
        _append_match(match_rows, seen_providers, scan_text, 'Alibaba (string)', 'alibaba', 'medium')

    urls = re.findall(r'https?://([^\s/"\']+)', scan_text)
    for url in urls:
        if 'amazonaws.com' in url or 'aws.amazon.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'AWS (URL)', 'aws', 'medium')
        if 'googleapis.com' in url or 'google.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Google (URL)', 'google', 'medium')
        if 'openai.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'OpenAI (URL)', 'openai', 'medium')
        if 'azure.com' in url or 'microsoft.com' in url or 'atlas.microsoft.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Azure (URL)', 'azure', 'medium')
        if 'aliyuncs.com' in url or 'alibaba' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Alibaba (URL)', 'alibaba', 'medium')
        if 'ibm.com' in url or 'watsonx.ibm.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'IBM (URL)', 'ibm', 'medium')
        if 'clarifai.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Clarifai (URL)', 'clarifai', 'medium')
        if 'launchdarkly' in url:
            _append_match(match_rows, seen_providers, scan_text, 'LaunchDarkly (URL)', 'launchdarkly', 'medium')
        if 'api.mapbox.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Mapbox (URL)', 'mapbox', 'medium')
        if 'hereapi.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'HERE (URL)', 'here', 'medium')
        if 'thehive.ai' in url or 'hive.ai' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Hive (URL)', 'hive', 'medium')
        if 'deepgram.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Deepgram (URL)', 'deepgram', 'medium')
        if 'elevenlabs.io' in url:
            _append_match(match_rows, seen_providers, scan_text, 'ElevenLabs (URL)', 'elevenlabs', 'medium')
        if 'mindee.net' in url or 'api.mindee.net' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Mindee (URL)', 'mindee', 'medium')
        if 'voyageai.com' in url or 'voyage.ai' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Voyage AI (URL)', 'voyage', 'medium')

    return match_rows


# ---------------------------------------------------------------------------
# Detection logic
# ---------------------------------------------------------------------------

def detect_provider_open(output_text):
    """Detect provider from open-ended (NLI/FIM) output.

    Returns (service, provider_key, ecosystem_key, confidence, detection_method).
    """
    if not output_text:
        return 'EMPTY', 'unknown', 'unknown', 'none', 'empty'

    matches = detect_provider_matches_open(output_text)
    if matches:
        primary = matches[0]
        return (
            primary["service"],
            primary["provider"],
            primary["ecosystem"],
            primary["confidence"],
            primary["method"],
        )

    return 'UNDETECTED', 'unknown', 'unknown', 'low', 'undetected'


def _score_cs_option(output_text, option):
    """Score how strongly the output matches a listed CS option."""
    output_lower = output_text.lower()
    score = 0
    evidence = []
    fields = [
        (option.get("label"), 3),
        (option.get("service"), 2),
        (option.get("sdk"), 2),
    ]
    for field, weight in fields:
        if field and field.lower() in output_lower:
            score += weight
            evidence.append(field)

    skeleton = option.get("skeleton", "")
    signatures = set()
    for token in re.findall(r"[A-Za-z_][A-Za-z0-9_\.]{2,}", skeleton):
        if len(token) >= 4:
            signatures.add(token.lower())
    for token in signatures:
        if token in output_lower:
            score += 1

    return score, evidence


def detect_provider_cs(output_text, scenario_data, prompt_meta=None):
    """Detect which CS option was chosen and whether it was listed or off-menu."""
    if not output_text:
        return {
            "detected_service": "EMPTY",
            "detected_provider": "unknown",
            "detected_ecosystem": "unknown",
            "detection_confidence": "none",
            "detection_method": "empty",
            "cs_choice_type": "undetected",
            "cs_selected_option_key": None,
            "cs_selected_option_label": None,
            "cs_selected_position": None,
        }

    scan_text = _strip_python_line_comments(output_text)
    options = scenario_data['options']
    order = (
        (prompt_meta or {}).get("reference_option_keys")
        or (prompt_meta or {}).get("cs_option_keys")
        or list(options.keys())
    )
    match_rows = detect_provider_matches_open(scan_text)
    direct_service, direct_provider, direct_ecosystem, direct_confidence, direct_method = detect_provider_open(scan_text)
    if direct_provider != "unknown":
        # "listed" must mean shown in this prompt, not merely present in the
        # scenario's full provider pool. Omission ablations intentionally keep
        # providers in scenario metadata while removing them from the rendered
        # reference-card order.
        choice_type = "listed" if direct_provider in order else "off_menu"
        result = {
            "detected_service": direct_service,
            "detected_provider": direct_provider,
            "detected_ecosystem": direct_ecosystem,
            "detection_confidence": direct_confidence,
            "detection_method": direct_method,
            "cs_choice_type": choice_type,
            "cs_selected_option_key": direct_provider if choice_type == "listed" else None,
            "cs_selected_option_label": options[direct_provider]["label"] if choice_type == "listed" and direct_provider in options else None,
            "cs_selected_position": order.index(direct_provider) + 1 if direct_provider in order else None,
            "cs_match_score": None,
            "cs_match_evidence": [],
        }
        result.update(summarize_provider_matches(match_rows))
        return result

    score_map = {}

    for provider_key in order:
        opt = options.get(provider_key)
        if not opt:
            continue
        score, evidence = _score_cs_option(scan_text, opt)
        score_map[provider_key] = {
            "score": score,
            "evidence": evidence,
            "label": opt.get("label", provider_key),
        }

    if score_map:
        ranked = sorted(score_map.items(), key=lambda kv: (kv[1]["score"], kv[0]), reverse=True)
        best_key, best = ranked[0]
        second_score = ranked[1][1]["score"] if len(ranked) > 1 else -1
        if best["score"] >= 3 and best["score"] > second_score:
            result = {
                "detected_service": best["label"],
                "detected_provider": best_key,
                "detected_ecosystem": PROVIDER_TO_ECOSYSTEM.get(best_key, best_key),
                "detection_confidence": "high" if best["score"] >= 5 else "medium",
                "detection_method": "cs_option_match",
                "cs_choice_type": "listed",
                "cs_selected_option_key": best_key,
                "cs_selected_option_label": best["label"],
                "cs_selected_position": order.index(best_key) + 1 if best_key in order else None,
                "cs_match_score": best["score"],
                "cs_match_evidence": best["evidence"],
            }
            result.update(summarize_provider_matches([{
                "service": best["label"],
                "provider": best_key,
                "ecosystem": PROVIDER_TO_ECOSYSTEM.get(best_key, best_key),
                "confidence": result["detection_confidence"],
                "method": "cs_option_match",
            }]))
            return result

    result = {
        "detected_service": "UNDETECTED",
        "detected_provider": "unknown",
        "detected_ecosystem": "unknown",
        "detection_confidence": "low",
        "detection_method": "undetected",
        "cs_choice_type": "undetected",
        "cs_selected_option_key": None,
        "cs_selected_option_label": None,
        "cs_selected_position": None,
        "cs_match_score": None,
        "cs_match_evidence": [],
    }
    result.update(summarize_provider_matches([]))
    return result


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def _hf_options_from_row(row):
    options = {}
    for tool in list(row.get("provider_tools", [])) + list(row.get("neutral_tools") or []):
        if not tool.get("eligible", True):
            continue
        provider_key = tool["provider_key"]
        options[provider_key] = {
            "label": tool.get("label") or tool.get("service") or provider_key,
            "service": tool.get("service") or tool.get("label") or provider_key,
            "sdk": tool.get("sdk") or "",
        }
    return options


def load_cs_scenario_data(benchmark="vibench"):
    """Load documented reference scenario data for listed/off-menu matching."""
    benchmark = _canonical_benchmark_name(benchmark)
    hf_path = DATASETS_DIR / benchmark / "direct" / "tasks.jsonl"
    if hf_path.exists():
        data = {}
        for line in hf_path.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            data[row["scenario_id"]] = {
                "scenario_id": row["scenario_id"],
                "options": _hf_options_from_row(row),
            }
        return data

    cs_dir = DATASETS_DIR / benchmark / 'cs_documented'
    data = {}
    if not cs_dir.exists():
        return data
    for f in cs_dir.glob('*.json'):
        with open(f) as fh:
            scenario = json.load(fh)
        data[scenario['scenario_id']] = scenario
    return data


def label_output(filepath, cs_scenarios):
    """Read a raw output file, detect the provider, return labeled record."""
    with open(filepath) as f:
        record = json.load(f)

    output_text = record.get('output_text', '') or ''
    modality = record.get('modality', '')
    task_id = record.get('task_id', '')

    # Extract scenario ID from task_id (e.g., nli_S04_a -> S04, cs_S04_r1 -> S04)
    scenario_match = re.search(r'S\d{2}', task_id)
    scenario_id = scenario_match.group() if scenario_match else None

    if _is_reference_modality(modality) and scenario_id in cs_scenarios:
        result = detect_provider_cs(output_text, cs_scenarios[scenario_id], record)
    else:
        match_rows = detect_provider_matches_open(output_text)
        service, provider, ecosystem, confidence, method = detect_provider_open(output_text)
        result = {
            "detected_service": service,
            "detected_provider": provider,
            "detected_ecosystem": ecosystem,
            "detection_confidence": confidence,
            "detection_method": method,
        }
        result.update(summarize_provider_matches(match_rows))

    record.update(result)
    if _is_reference_modality(modality):
        record.setdefault("reference_choice_type", record.get("cs_choice_type"))
        record.setdefault("reference_selected_option_key", record.get("cs_selected_option_key"))
        record.setdefault("reference_selected_option_label", record.get("cs_selected_option_label"))
        record.setdefault("reference_selected_position", record.get("cs_selected_position"))
        record.setdefault("reference_match_score", record.get("cs_match_score"))
        record.setdefault("reference_match_evidence", record.get("cs_match_evidence"))
    return record


def run_detection(run_dir, modality_filter=None):
    """Label all raw outputs in a run and save to labeled/ within that run."""
    # Detect benchmark version from run config
    run_config_path = run_dir / "config.yaml"
    benchmark = "vibench"
    if run_config_path.exists():
        try:
            import yaml
            with open(run_config_path) as _f:
                _cfg = yaml.safe_load(_f) or {}
            benchmark = _cfg.get("benchmark", "vibench")
        except ModuleNotFoundError:
            config_text = run_config_path.read_text()
            match = re.search(r'(?m)^benchmark:\s*([A-Za-z0-9_.-]+)\s*$', config_text)
            if match:
                benchmark = match.group(1)
    cs_scenarios = load_cs_scenario_data(benchmark=benchmark)
    raw_base = run_dir / "raw"
    labeled_base = run_dir / "labeled"

    if modality_filter:
        modalities = [modality_filter]
    else:
        modalities = ['nli', 'fim', OPEN_REFERENCE_MODALITY, LEGACY_CS_MODALITY]
    total = 0
    detected = 0
    by_confidence = Counter()
    by_provider = Counter()
    by_ecosystem = Counter()
    by_method = Counter()
    by_choice_type = Counter()
    multi_provider = 0
    multi_ecosystem = 0

    for modality in modalities:
        raw_mod_dir = raw_base / modality
        if not raw_mod_dir.exists():
            print(f"  No outputs for {modality} (skipping)")
            continue

        # Support both structures:
        #   new: raw/{modality}/{model_id}/{task_id}__c{N}.json
        #   old: raw/{modality}/{task_id}__{model_id}__c{N}.json
        raw_files = []
        for model_dir in sorted(raw_mod_dir.iterdir()):
            if model_dir.is_dir():
                # New structure: model subdirectory
                for f in sorted(model_dir.glob('*.json')):
                    raw_files.append((f, model_dir.name))
            elif model_dir.suffix == '.json':
                # Old flat structure
                raw_files.append((model_dir, None))

        for f, model_subfolder in raw_files:
            record = label_output(f, cs_scenarios)
            total += 1

            provider = record['detected_provider']
            ecosystem = record.get('detected_ecosystem', 'unknown')
            confidence = record['detection_confidence']
            method = record.get('detection_method', 'unknown')
            by_confidence[confidence] += 1
            by_provider[provider] += 1
            by_ecosystem[ecosystem] += 1
            by_method[method] += 1
            multi_provider += int(bool(record.get("is_multi_provider")))
            multi_ecosystem += int(bool(record.get("is_multi_ecosystem")))
            if _is_reference_modality(modality):
                by_choice_type[
                    record.get("reference_choice_type") or record.get("cs_choice_type", "unknown")
                ] += 1

            if provider != 'unknown':
                detected += 1

            # Mirror the folder structure in labeled/
            if model_subfolder:
                labeled_dir = labeled_base / modality / model_subfolder
            else:
                labeled_dir = labeled_base / modality
            labeled_dir.mkdir(parents=True, exist_ok=True)
            out_path = labeled_dir / f.name
            with open(out_path, 'w') as fh:
                json.dump(record, fh, indent=2, ensure_ascii=False)

    print(f"\nRun: {run_dir.name}")
    print(f"Detection complete:")
    print(f"  Total outputs:  {total}")
    print(f"  Detected:       {detected} ({detected/total:.0%})" if total > 0 else "  No outputs found")
    print(f"  Undetected:     {total - detected}")
    print(f"\n  By confidence:  {dict(by_confidence)}")
    print(f"  By provider:    {dict(by_provider)}")
    print(f"  By ecosystem:   {dict(by_ecosystem)}")
    print(f"  By method:      {dict(by_method)}")
    print(f"  Multi-provider: {multi_provider} ({multi_provider/total:.1%})" if total > 0 else "  Multi-provider: 0")
    print(f"  Multi-ecosystem:{multi_ecosystem} ({multi_ecosystem/total:.1%})" if total > 0 else "  Multi-ecosystem: 0")
    if by_choice_type:
        print(f"  CS choices:     {dict(by_choice_type)}")


def print_stats(run_dir):
    """Print stats from already-labeled outputs in a run."""
    labeled_base = run_dir / "labeled"
    if not labeled_base.exists():
        print(f"No labeled outputs in {run_dir.name}. Run detection first.")
        return

    from collections import defaultdict
    all_records = []
    for modality_dir in sorted(labeled_base.iterdir()):
        if modality_dir.is_dir():
            # Collect from both flat and nested structures
            for f in sorted(modality_dir.rglob('*.json')):
                with open(f) as fh:
                    all_records.append(json.load(fh))

    if not all_records:
        print("No labeled outputs found.")
        return

    print(f"Run: {run_dir.name}")
    print(f"Total labeled outputs: {len(all_records)}\n")

    model_provider = defaultdict(Counter)
    model_ecosystem = defaultdict(Counter)
    modality_provider = defaultdict(Counter)
    modality_ecosystem = defaultdict(Counter)

    for r in all_records:
        model_provider[r.get('model_id', '?')][r.get('detected_provider', '?')] += 1
        model_ecosystem[r.get('model_id', '?')][r.get('detected_ecosystem', r.get('detected_provider', '?'))] += 1
        modality_provider[r.get('modality', '?')][r.get('detected_provider', '?')] += 1
        modality_ecosystem[r.get('modality', '?')][r.get('detected_ecosystem', r.get('detected_provider', '?'))] += 1

    print("=== Provider distribution per model ===")
    for model in sorted(model_provider):
        total = sum(model_provider[model].values())
        parts = ', '.join(f"{p}:{c}" for p, c in model_provider[model].most_common())
        print(f"  {model:25s} ({total:3d}): {parts}")

    print("\n=== Ecosystem distribution per model ===")
    for model in sorted(model_ecosystem):
        total = sum(model_ecosystem[model].values())
        parts = ', '.join(f"{p}:{c}" for p, c in model_ecosystem[model].most_common())
        print(f"  {model:25s} ({total:3d}): {parts}")

    print("\n=== Provider distribution per modality ===")
    for mod in sorted(modality_provider):
        total = sum(modality_provider[mod].values())
        parts = ', '.join(f"{p}:{c}" for p, c in modality_provider[mod].most_common())
        print(f"  {mod:15s} ({total:3d}): {parts}")

    print("\n=== Ecosystem distribution per modality ===")
    for mod in sorted(modality_ecosystem):
        total = sum(modality_ecosystem[mod].values())
        parts = ', '.join(f"{p}:{c}" for p, c in modality_ecosystem[mod].most_common())
        print(f"  {mod:15s} ({total:3d}): {parts}")


def main():
    parser = argparse.ArgumentParser(description="VIBench Service Detection Pipeline")
    parser.add_argument("--run", type=str, nargs="+", default=["latest"],
                        help="Run ID(s) or 'latest'. Multiple runs are processed independently.")
    parser.add_argument("--modality", choices=["nli", "fim", OPEN_REFERENCE_MODALITY, LEGACY_CS_MODALITY],
                        help="Label only this modality")
    parser.add_argument("--stats", action="store_true",
                        help="Print stats from already-labeled outputs")
    args = parser.parse_args()

    for run_id in args.run:
        run_dir = resolve_run_dir(run_id)
        if not run_dir:
            continue
        if args.stats:
            print_stats(run_dir)
        else:
            run_detection(run_dir, args.modality)


if __name__ == "__main__":
    main()
