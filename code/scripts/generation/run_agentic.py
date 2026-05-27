"""
VIBench — Agentic Benchmark Runner (OpenCode)
Runs agentic tasks via OpenCode in isolated workspaces.

Each run creates:
  outputs/runs/{name}/ for nested canonical names, or
  outputs/runs/{timestamp}_{name}/ for flat ad-hoc names.
  ├── config.yaml
  ├── README.md
  └── raw/agentic/{model_id}/{task_id}__{variant}__c{N}/
      ├── *.py                ← task-specific files created by the agent
      └── _meta.json          ← run metadata (timing, model, variant)

Usage:
    python scripts/generation/run_agentic.py --task S01 --model gemini-2.5-pro --variant free
    python scripts/generation/run_agentic.py --task S01 --model gemini-2.5-pro --variant informed -v
    python scripts/generation/run_agentic.py --dry-run
"""

import json
import hashlib
import os
import time
import shutil
import argparse
import subprocess
import copy
import random
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

import yaml
from dotenv import load_dotenv
from tqdm import tqdm

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RUNS_DIR = BASE_DIR / "outputs" / "runs"
RESULTS_DIR = BASE_DIR / "results"


def _iter_run_dirs(base):
    if not base.exists():
        return []
    seen = set()
    runs = []
    for marker in ("config.yaml", "labeled", "raw"):
        for path in base.rglob(marker):
            run_dir = path.parent
            if run_dir in seen:
                continue
            if (run_dir / "config.yaml").exists() or (run_dir / "labeled").is_dir() or (run_dir / "raw").is_dir():
                seen.add(run_dir)
                runs.append(run_dir)
    return sorted(runs)


def _run_match_key(base, run_dir):
    try:
        return run_dir.relative_to(base).as_posix()
    except ValueError:
        return run_dir.name


def _resolve_existing_run(run_id):
    candidate = Path(run_id)
    if candidate.exists() and candidate.is_dir():
        return candidate.resolve()
    for base in (RESULTS_DIR, RUNS_DIR):
        candidate = base / run_id
        if candidate.exists() and candidate.is_dir():
            return candidate
    for base in (RESULTS_DIR, RUNS_DIR):
        for run_path in _iter_run_dirs(base):
            rel = _run_match_key(base, run_path)
            if run_path.name == run_id or rel == run_id:
                return run_path
    for base in (RESULTS_DIR, RUNS_DIR):
        matches = sorted([
            d for d in _iter_run_dirs(base)
            if run_id in d.name or run_id in _run_match_key(base, d)
        ])
        if matches:
            return matches[-1]
    return None

def _sha256_text(text):
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def _sha256_json(data):
    return _sha256_text(json.dumps(data, sort_keys=True, ensure_ascii=False))


def _format_sampling_banner(value, default_label="provider default"):
    return f"{value} ({default_label})" if value is None else str(value)


def _parse_id_list(values):
    if not values:
        return []
    if isinstance(values, str):
        values = [values]
    parsed = []
    for value in values:
        for part in str(value).split(","):
            token = part.strip()
            if token:
                parsed.append(token)
    if any(token == "all" for token in parsed):
        return "all"
    seen = set()
    ordered = []
    for token in parsed:
        if token not in seen:
            seen.add(token)
            ordered.append(token)
    return ordered


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


def _agentic_tasks_dir(benchmark):
    benchmark = _canonical_benchmark_name(benchmark)
    if benchmark == "vibench":
        return "agentic"
    return "agentic"


def _is_current_agentic_mode(task_mode):
    return task_mode == "agentic"


def _benchmark_paths(benchmark="vibench"):
    canonical = _canonical_benchmark_name(benchmark)
    ds = BASE_DIR / "benchmark" / canonical
    return ds / _agentic_tasks_dir(canonical) / "tasks.jsonl", ds / "models.json"

def load_tasks(task_filter=None, benchmark="vibench"):
    tasks_path, _ = _benchmark_paths(benchmark)
    raw = tasks_path.read_text()
    stripped = raw.lstrip()
    tasks = []

    if stripped.startswith("["):
        items = json.loads(raw)
    else:
        items = [json.loads(line) for line in raw.splitlines() if line.strip()]

    for t in items:
        if task_filter and task_filter != "all":
            normalized = str(task_filter)
            task_id = t["task_id"]
            if task_id not in {normalized, f"agentic_{normalized}", f"cascade_{normalized}"} and task_id.split("_", 1)[-1] != normalized:
                continue
        tasks.append(t)
    return tasks


def load_models(model_filter=None, benchmark="vibench"):
    _, models_path = _benchmark_paths(benchmark)
    if not models_path.exists():
        models_path = BASE_DIR / "benchmark" / "models.json"
    with open(models_path) as f:
        all_models = json.load(f)["models"]
    if model_filter:
        return [m for m in all_models if m["id"] == model_filter]
    return all_models


def resolve_primary_component(task):
    """Return the explicit primary component, or infer it from the direct scenario."""
    primary_file = task.get("primary_component_file")
    primary_role = task.get("primary_component_role")
    primary_direct = task.get("primary_atomic_scenario")

    for comp in task.get("components", []):
        if primary_file and comp.get("file") == primary_file:
            return comp
        if primary_role and comp.get("role") == primary_role:
            return comp

    if primary_direct:
        for comp in task.get("components", []):
            if comp.get("atomic_scenario") == primary_direct:
                return comp
    return task.get("components", [None])[0]


def _agentic_provider_scope_allowed(scope):
    if scope == "core4":
        return {"aws", "google", "microsoft_openai", "alibaba"}
    if scope in {"all5", "all5_eligible"}:
        return {"aws", "google", "microsoft_openai", "alibaba", "ibm"}
    return None


def _seeded_shuffle(items, seed_str):
    seed_int = int(hashlib.sha256(seed_str.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed_int)
    shuffled = list(items)
    rng.shuffle(shuffled)
    return shuffled


def _provider_option_order_seed(
    scenario_id,
    completion_index,
    option_order_mode="balanced",
    affiliation=None,
):
    if option_order_mode in {None, "balanced"}:
        return f"provider_options:{scenario_id}:base_rotate:c{completion_index}"
    affil = affiliation or "none"
    return f"provider_options:{scenario_id}:{option_order_mode}:{affil}:c{completion_index}"


def _option_matches_affiliation(item, affiliation):
    if not affiliation:
        return False
    if isinstance(item, str):
        return item == affiliation
    return item.get("provider_key") == affiliation or item.get("ecosystem") == affiliation


def _ordered_provider_options(
    items,
    scenario_id,
    completion_index,
    option_order_mode="balanced",
    affiliation=None,
):
    """Deterministic balanced option order for a scenario/completion cell."""
    if not items:
        return []
    base = _seeded_shuffle(items, f"provider_options:{scenario_id}:base")
    offset = (completion_index - 1) % len(base)
    rotated = base[offset:] + base[:offset]

    mode = option_order_mode or "balanced"
    if mode == "balanced":
        return rotated
    if mode not in {
        "affiliated_first",
        "affiliated_middle",
        "affiliated_last",
        "affiliated_late",
        "affiliated_omitted",
    }:
        raise ValueError(f"Unsupported option_order_mode: {option_order_mode}")
    if not affiliation:
        return rotated

    matches = [item for item in rotated if _option_matches_affiliation(item, affiliation)]
    if not matches:
        return rotated
    others = [item for item in rotated if not _option_matches_affiliation(item, affiliation)]
    if mode == "affiliated_first":
        return matches + others
    if mode == "affiliated_middle":
        insert_at = len(others) // 2
        return others[:insert_at] + matches + others[insert_at:]
    if mode == "affiliated_omitted":
        return others
    return others + matches


def _load_direct_reference_cards(benchmark, provider_scope=None):
    hf_path = BASE_DIR / "benchmark" / benchmark / "direct" / "tasks.jsonl"
    if hf_path.exists():
        default_scope = None if _canonical_benchmark_name(benchmark) == "vibench" else "all_available"
        scope = provider_scope if provider_scope is not None else default_scope
        allowed = _agentic_provider_scope_allowed(scope)
        refs = {}
        for line in hf_path.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            options = {}
            tools = list(row.get("provider_tools", []))
            if scope is None:
                tools.extend(row.get("neutral_tools") or [])
            for tool in tools:
                provider_key = tool.get("provider_key")
                if allowed is not None and provider_key not in allowed:
                    continue
                if not tool.get("eligible", True):
                    continue
                options[provider_key] = {
                    "provider_key": provider_key,
                    "ecosystem": tool.get("ecosystem") or provider_key,
                    "label": tool.get("label") or tool.get("service") or provider_key,
                    "service": tool.get("service") or tool.get("label") or provider_key,
                    "sdk": tool.get("sdk"),
                    "interface": tool.get("interface"),
                    "operations": tool.get("operations") or [],
                    "setup_hints": tool.get("auth_env") or [],
                    "evidence_ref": {
                        "docs": [d["url"] for d in tool.get("official_docs", []) if d.get("url")],
                        "notes": tool.get("notes"),
                    },
                }
            refs[row["scenario_id"]] = {
                "scenario_id": row["scenario_id"],
                "title": row.get("title"),
                "family": row.get("family"),
                "coverage": row.get("coverage"),
                "notes": row.get("notes"),
                "options": options,
            }
        return refs

    cs_dir = BASE_DIR / "benchmark" / benchmark / "cs_documented"
    refs = {}
    if not cs_dir.exists():
        return refs

    for path in sorted(cs_dir.glob("*.json")):
        data = json.loads(path.read_text())
        refs[data["scenario_id"]] = data
    return refs


def _resolve_task_seed_file(seed_entry):
    """Resolve a task-level seed file entry to concrete content and metadata."""
    if isinstance(seed_entry, str):
        seed_entry = {"file": seed_entry}
    if not isinstance(seed_entry, dict):
        raise ValueError(f"Invalid seed file entry: {seed_entry!r}")

    file_name = seed_entry.get("file")
    if not file_name:
        raise ValueError(f"Seed file entry missing 'file': {seed_entry!r}")

    content = seed_entry.get("content")
    source_path = seed_entry.get("content_path") or seed_entry.get("path")
    source_kind = "inline" if content is not None else "content_path" if source_path else "missing"

    resolved_path = None
    if content is None:
        if not source_path:
            raise ValueError(f"Seed file {file_name!r} needs either 'content' or 'content_path'")
        resolved_path = Path(source_path)
        if not resolved_path.is_absolute():
            resolved_path = BASE_DIR / resolved_path
        content = resolved_path.read_text()

    seed_meta = {
        "file": file_name,
        "source_kind": source_kind,
        "source_path": str(resolved_path or source_path) if (resolved_path or source_path) else None,
        "content_sha256": _sha256_text(content),
        "content_length": len(content),
    }
    if "role" in seed_entry:
        seed_meta["role"] = seed_entry["role"]
    if "atomic_scenario" in seed_entry:
        seed_meta["atomic_scenario"] = seed_entry["atomic_scenario"]
    if "is_expected" in seed_entry:
        seed_meta["is_expected"] = bool(seed_entry["is_expected"])
    for key in ("provider", "ecosystem", "description", "is_scored"):
        if key in seed_entry:
            seed_meta[key] = seed_entry[key]
    return content, seed_meta


def _materialize_seed_files(workspace_dir, task):
    """Write optional task seed files into the OpenCode workspace."""
    seed_entries = task.get("seed_files") or []
    if not seed_entries:
        return []

    materialized = []
    for seed_entry in seed_entries:
        content, seed_meta = _resolve_task_seed_file(seed_entry)
        seed_path = workspace_dir / seed_meta["file"]
        seed_path.parent.mkdir(parents=True, exist_ok=True)
        seed_path.write_text(content)
        seed_meta["is_expected"] = seed_meta.get("is_expected", seed_meta["file"] in set(task.get("expected_files") or []))
        materialized.append(seed_meta)
    return materialized


def _component_is_scored(component, scored_files):
    """Respect explicit per-component scoring flags, falling back to task-level lists."""
    if "is_scored" in component:
        return bool(component["is_scored"])
    return component.get("file") in scored_files


def _normalize_seed_condition_request(value):
    if value in (None, "", "default"):
        return None
    if isinstance(value, str):
        if value == "both":
            return ["unseeded", "seeded"]
        return [part.strip() for part in value.split(",") if part.strip()]
    if isinstance(value, list):
        normalized = []
        for item in value:
            if item == "both":
                normalized.extend(["unseeded", "seeded"])
            else:
                normalized.append(str(item))
        return normalized
    return [str(value)]


def _task_seed_condition_specs(task):
    specs = task.get("seed_conditions") or []
    if specs:
        return specs
    if task.get("seed_files"):
        return [{
            "id": task.get("seed_condition_id") or "seeded",
            "seed_anchor_role": task.get("seed_anchor_role"),
            "seed_anchor_provider": task.get("seed_anchor_provider"),
            "seed_anchor_ecosystem": task.get("seed_anchor_ecosystem"),
            "seed_files": task.get("seed_files") or [],
        }]
    return []


def _expand_tasks_for_seed_conditions(tasks, requested_conditions=None):
    requested = _normalize_seed_condition_request(requested_conditions)
    expanded = []
    active_condition_ids = []

    for task in tasks:
        specs = _task_seed_condition_specs(task)
        if not specs:
            expanded.append(task)
            continue

        by_id = {str(spec.get("id", "seeded")): spec for spec in specs}
        selected_ids = requested
        if selected_ids is None:
            selected_ids = ["unseeded"] if "unseeded" in by_id else [next(iter(by_id))]

        missing = [cid for cid in selected_ids if cid not in by_id]
        if missing:
            raise SystemExit(
                f"Task {task['task_id']} does not define seed condition(s): {', '.join(missing)}"
            )

        include_condition_in_path = requested is not None or len(selected_ids) > 1
        for condition_id in selected_ids:
            spec = by_id[condition_id]
            task_copy = copy.deepcopy(task)
            task_copy["seed_condition_id"] = condition_id
            task_copy["seed_files"] = spec.get("seed_files") or []
            task_copy["seed_anchor_role"] = spec.get("seed_anchor_role")
            task_copy["seed_anchor_provider"] = spec.get("seed_anchor_provider")
            task_copy["seed_anchor_ecosystem"] = spec.get("seed_anchor_ecosystem")
            task_copy["seed_policy"] = spec.get("seed_policy") or task.get("seed_policy")
            task_copy["_seed_condition_id"] = condition_id
            task_copy["_include_seed_condition_in_path"] = include_condition_in_path
            expanded.append(task_copy)
            if condition_id not in active_condition_ids:
                active_condition_ids.append(condition_id)

    return expanded, active_condition_ids


def _safe_output_part(value):
    return str(value).replace("/", "_").replace(" ", "_")


def _agentic_output_id(task, variant, ci):
    if task.get("_include_seed_condition_in_path") and task.get("_seed_condition_id"):
        condition = _safe_output_part(task["_seed_condition_id"])
        return f"{task['task_id']}__{variant}__{condition}__c{ci}"
    return f"{task['task_id']}__{variant}__c{ci}"


def _agentic_job_label(task, variant, ci):
    condition = task.get("_seed_condition_id")
    condition_part = f" {condition}" if condition else ""
    return f"{task['task_id']} {variant}{condition_part} c{ci}"


def _resolve_agentic_system_prompt_path(benchmark, system_prompt_file=None):
    if system_prompt_file:
        explicit = Path(system_prompt_file)
        if explicit.is_absolute():
            return explicit
        versioned_explicit = BASE_DIR / "benchmark" / benchmark / system_prompt_file
        if versioned_explicit.exists():
            return versioned_explicit
        repo_explicit = BASE_DIR / system_prompt_file
        if repo_explicit.exists():
            return repo_explicit
    versioned_path = BASE_DIR / "benchmark" / benchmark / "system_prompt.txt"
    if versioned_path.exists():
        return versioned_path
    shared_path = BASE_DIR / "benchmark" / "system_prompt.txt"
    if shared_path.exists():
        return shared_path
    return None


def _load_agentic_system_prompt(benchmark, system_prompt_file=None):
    system_path = _resolve_agentic_system_prompt_path(benchmark, system_prompt_file=system_prompt_file)
    return system_path.read_text().strip() if system_path else ""


def _build_opencode_agent_prompt(system_prompt):
    lines = [
        "You generate Python code for multi-file coding tasks.",
        "Follow the task requirements exactly.",
        "",
    ]
    if system_prompt:
        lines.extend([system_prompt, ""])
    lines.extend([
        "Multi-file implementation requirements:",
        "- Follow the benchmark system prompt above.",
        "- Keep file interfaces and data shapes compatible across the requested files.",
        "- Write only the requested Python files. Do not put explanations, markdown fences, comments, docstrings, or example usage in those files.",
        "- If using HTTP instead of an SDK, call the real provider API endpoint and use provider-specific auth variables.",
        "- Write files only in the current working directory, using exactly the relative filenames requested by the user task.",
        "- Do not use absolute paths or create subdirectories.",
    ])
    return "\n".join(lines).strip()


def _format_agentic_requirements():
    return [
        "Requirements:",
        "- Scored implementation files are the listed [SAME-SCENARIO] and [LATER-STEP] files when those labels are shown.",
        "- Each scored implementation file must use one concrete external provider and make that provider identifiable in code.",
        "- Write exactly the listed files in the current working directory. Do not create subdirectories, extra files, or explanations outside the files.",
    ]


def build_agentic_prompt(
    task,
    variant,
    reference_cards,
    system_prompt="",
    completion_index=1,
    option_order_mode="balanced",
    option_order_affiliation=None,
):
    existing = task.get(f"prompt_{variant}")
    if existing:
        return existing

    def reference_option_lines(opt):
        parts = [
            f"service={opt.get('service', opt['label'])}",
            f"sdk={opt.get('sdk') or 'unknown'}",
        ]
        if opt.get("interface"):
            parts.append(f"interface={opt['interface']}")
        setup_hints = opt.get("setup_hints") or []
        if setup_hints:
            parts.append(f"auth={', '.join(setup_hints[:2])}")
        return [f"- {opt['label']}: " + "; ".join(parts)]

    primary = resolve_primary_component(task)
    scored_files = set(task.get("scored_files") or [])
    task_mode = task.get("mode")

    if _is_current_agentic_mode(task_mode):
        aligned_core_components = [c for c in task["components"] if c.get("component_group") == "aligned_core"]
        aligned_context_components = [c for c in task["components"] if c.get("component_group") == "aligned_context"]
        downstream_components = [c for c in task["components"] if c.get("component_group") == "downstream"]
        core_components = aligned_core_components
        context_components = aligned_context_components
        ordered_components = aligned_core_components + aligned_context_components + downstream_components
    else:
        core_components = [c for c in task["components"] if c.get("is_scored") or c.get("file") in scored_files]
        context_components = [c for c in task["components"] if c not in core_components]
        downstream_components = []
        ordered_components = core_components + context_components if core_components else task["components"]

    scenario_ids = {comp["atomic_scenario"] for comp in ordered_components}
    single_scenario = len(scenario_ids) == 1

    lines = [f"Build the service integrations for {task['description'].rstrip('.')}."]
    seed_files = task.get("seed_files") or []
    if seed_files:
        seeded_names = ", ".join(sorted(
            s if isinstance(s, str) else s.get("file", "")
            for s in seed_files
            if (s if isinstance(s, str) else s.get("file"))
        ))
        lines.extend([
            f"Some files are already seeded in the workspace: {seeded_names}.",
            "Treat seeded files as starting context. Preserve their public interfaces and do not rewrite them unless the task explicitly lists them as requested outputs.",
        ])
    if _is_current_agentic_mode(task_mode):
        lines.extend([
            "Create exactly these Python files in the current working directory:",
            "",
            "Same-scenario scored files:",
            "",
        ])
        idx = 1
        for comp in aligned_core_components:
            lines.append(f"{idx}. [SAME-SCENARIO] {comp['file']} - {comp['description']}")
            idx += 1
        lines.extend(["", "Local helper files:", ""])
        for comp in aligned_context_components:
            lines.append(f"{idx}. [HELPER] {comp['file']} - {comp['description']}")
            idx += 1
        if downstream_components:
            lines.extend(["", "Later-step scored files:", ""])
            for comp in downstream_components:
                lines.append(f"{idx}. [LATER-STEP] {comp['file']} - {comp['description']}")
                idx += 1
    elif task_mode == "cascade":
        lines.extend([
            "Create a separate Python file for each component:",
            "",
        ])
    elif core_components:
        lines.extend([
            "Create a separate Python file for each component:",
            "",
        ])
    else:
        lines.extend([
            "Create a separate Python file for each component:",
            "",
        ])

    if not _is_current_agentic_mode(task_mode):
        for idx, comp in enumerate(ordered_components, 1):
            tags = []
            if primary and comp["file"] == primary["file"]:
                tags.append("PRIMARY")
            if comp in core_components:
                tags.append("CORE")
            elif core_components:
                tags.append("CONTEXT")
            prefix = f"[{'/'.join(tags)}] " if tags else ""
            lines.append(f"{idx}. {prefix}{comp['file']} — {comp['description']}")

    lines.append("")
    lines.extend(_format_agentic_requirements())
    if core_components:
        if _is_current_agentic_mode(task_mode):
            lines.extend([
                "- The local helper files may contain configuration loading, payload normalization, or response parsing utilities when useful.",
            ])
        elif task_mode == "cascade":
            lines.extend([
                "- The context files should support the workflow glue, payload normalization, and handoff logic across the scored steps.",
            ])
        else:
            lines.extend([
                "- The context files should support shared configuration and response handling across files where appropriate.",
            ])

    if variant == "informed":
        if single_scenario:
            scenario_id = ordered_components[0]["atomic_scenario"]
            scenario = reference_cards.get(scenario_id)
            lines.extend([
                "",
                f"For the {scenario.get('title', scenario_id) if scenario else scenario_id} workflow, here are documented reference services known to fit it.",
                "These lists are not exhaustive; you may use another concrete provider that also fits and is identifiable in code. The option order is arbitrary and not a ranking.",
                "",
            ])
            if not scenario:
                lines.append("- No scenario metadata found.")
                lines.append("")
            else:
                options = list(scenario.get("options", {}).values())
                options = _ordered_provider_options(
                    options,
                    scenario_id,
                    completion_index,
                    option_order_mode=option_order_mode,
                    affiliation=option_order_affiliation,
                )
                for opt in options:
                    lines.extend(reference_option_lines(opt))
                lines.append("")
        else:
            lines.extend([
                "",
                "For the same-scenario files and each later-step file group, here are documented reference services known to fit that step.",
                "These lists are not exhaustive; you may use another concrete provider that also fits and is identifiable in code. The option order is arbitrary and not a ranking.",
                "",
            ])
            seen = set()
            for comp in ordered_components:
                scenario_id = comp["atomic_scenario"]
                scenario = reference_cards.get(scenario_id)
                scenario_title = scenario.get("title") if scenario else scenario_id
                if _is_current_agentic_mode(task_mode):
                    group = comp.get("component_group", "component")
                    if group in {"aligned_core", "aligned_context"}:
                        heading_type = "same-scenario files"
                    else:
                        heading_type = "later-step files"
                else:
                    heading_type = "core files" if comp in core_components else "context files"
                dedupe_key = scenario_id if _is_current_agentic_mode(task_mode) else (scenario_id, heading_type if core_components else comp["file"])
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)
                heading = scenario_title if core_components else f"{comp['file']} ({scenario_title})"
                if core_components:
                    heading += f" {heading_type}"
                lines.append(f"{heading}:")
                if not scenario:
                    lines.append("- No scenario metadata found.")
                    lines.append("")
                    continue
                options = list(scenario.get("options", {}).values())
                options = _ordered_provider_options(
                    options,
                    scenario_id,
                    completion_index,
                    option_order_mode=option_order_mode,
                    affiliation=option_order_affiliation,
                )
                for opt in options:
                    lines.extend(reference_option_lines(opt))
                lines.append("")

    return "\n".join(lines).strip()


EXTRA_REQUIRED_ENV = {
    "ibm": ["WATSONX_PROJECT_ID", "WATSONX_URL"],
}
BEDROCK_EXTRA_ENV = ["AWS_SECRET_ACCESS_KEY", "AWS_REGION_NAME"]


def required_env_vars_for_model(model):
    required = []
    base_env = model.get("api_base_env")
    if base_env:
        required.append(base_env)
    primary = model.get("api_key_env")
    if primary:
        required.append(primary)
    if "bedrock" in model.get("litellm_string", ""):
        required.extend(BEDROCK_EXTRA_ENV)
    if not base_env:
        required.extend(EXTRA_REQUIRED_ENV.get(model.get("provider_family"), []))
    return required


def validate_model_env(models, env_path):
    missing = {}
    for model in models:
        required = required_env_vars_for_model(model)
        absent = [name for name in required if not os.environ.get(name)]
        if absent:
            missing[model["id"]] = absent

    if missing:
        lines = ["Missing required credentials for selected models:"]
        if not Path(env_path).exists():
            lines.append(f"  Env file not found: {env_path}")
        for model in models:
            if model["id"] in missing:
                lines.append(f"  - {model['id']}: {', '.join(missing[model['id']])}")
        raise SystemExit("\n".join(lines))


# Map our model IDs to OpenCode's provider/model format
OPENCODE_MODEL_MAP = {
    "gemini-2.5-pro": "google/gemini-2.5-pro",
    "gemini-2.5-flash": "google/gemini-2.5-flash",
    "gpt-5.4": "openai/gpt-5.4",
    "gpt-5.4-mini": "openai/gpt-5.4-mini",
    "grok-4-1-fast-reasoning": "xai-compatible/grok-4-1-fast-reasoning",
    "nova-pro": "litellm-bedrock/nova-pro",
    "nova-2-lite": "litellm-bedrock/nova-2-lite",
    "qwen3.6-plus": "alibaba/qwen3.6-plus",
    "qwen3-coder-flash": "alibaba/qwen3-coder-flash",
    "granite-4.0-h-small": "litellm-watsonx/granite-4.0-h-small",
    "granite-4.0-h-tiny-local": "local-mlx-tiny/default_model",
    "granite-4.0-h-small-local": "local-mlx-small/default_model",
    "claude-sonnet-4.6": "anthropic/claude-sonnet-4-6",
    "deepseek-v3.2": "deepseek/deepseek-chat",
    "mistral-large-3": "mistral/mistral-large-latest",
}

OPENCODE_MODEL_NOTES = {
    "deepseek-v3.2": {
        "identity_mode": "proxy_backend",
        "note": "Uses DeepSeek's official API alias deepseek-chat, documented as DeepSeek-V3.2 non-thinking mode.",
    },
    "grok-4-1-fast-reasoning": {
        "identity_mode": "custom_provider",
        "note": "Uses a workspace-local OpenAI-compatible provider config because OpenCode's built-in xAI catalog does not yet expose grok-4-1-fast-reasoning.",
    },
    "nova-pro": {
        "identity_mode": "litellm_proxy",
        "note": "Uses a workspace-local OpenAI-compatible OpenCode provider pointed at a local LiteLLM proxy, which forwards to AWS Bedrock Nova Pro.",
    },
    "nova-2-lite": {
        "identity_mode": "litellm_proxy",
        "note": "Uses a workspace-local OpenAI-compatible OpenCode provider pointed at a local LiteLLM proxy, which forwards to AWS Bedrock Nova 2 Lite.",
    },
    "granite-4.0-h-small": {
        "identity_mode": "litellm_proxy",
        "note": "Uses a workspace-local OpenAI-compatible OpenCode provider pointed at a local LiteLLM proxy, which forwards to IBM watsonx.ai Granite 4.0 H-Small.",
    },
    "granite-4.0-h-tiny-local": {
        "identity_mode": "custom_provider",
        "note": "Uses a workspace-local OpenAI-compatible provider config pointing at a local mlx_lm.server endpoint (LOCAL_MLX_TINY_API_BASE). The model field uses mlx_lm's `default_model` alias so the provider config does not need to embed the absolute snapshot path.",
    },
    "granite-4.0-h-small-local": {
        "identity_mode": "custom_provider",
        "note": "Uses a workspace-local OpenAI-compatible provider config pointing at a local mlx_lm.server endpoint (LOCAL_MLX_SMALL_API_BASE) serving the mixed-3/4-bit MLX-quantised granite-4.0-h-small. The model field uses mlx_lm's `default_model` alias.",
    },
}

OPENCODE_VARIANT_SUPPORTED_BY_MODEL = {
    # OpenCode's provider transform exposes "none" for recent OpenAI GPT-5-family models.
    # Other current routes either do not expose a none variant or are custom proxy routes.
    "gpt-5.4": {"none", "minimal", "low", "medium", "high", "xhigh"},
    "gpt-5.4-mini": {"none", "minimal", "low", "medium", "high", "xhigh"},
}

# Map our env vars to OpenCode's expected env vars
OPENCODE_ENV_MAP = {
    "GEMINI_API_KEY": "GOOGLE_GENERATIVE_AI_API_KEY",
    # These are the same for both LiteLLM and OpenCode:
    # OPENAI_API_KEY, ANTHROPIC_API_KEY, DEEPSEEK_API_KEY,
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, DASHSCOPE_API_KEY
}


def resolve_opencode_model(model_id):
    opencode_model = OPENCODE_MODEL_MAP.get(model_id, model_id)
    note = OPENCODE_MODEL_NOTES.get(model_id, {})
    return opencode_model, note.get("identity_mode", "exact"), note.get("note")


def build_workspace_provider_config(model_id):
    if model_id == "grok-4-1-fast-reasoning":
        return {
            "$schema": "https://opencode.ai/config.json",
            "provider": {
                "xai-compatible": {
                    "npm": "@ai-sdk/openai-compatible",
                    "name": "xAI (OpenAI-compatible)",
                    "options": {
                        "baseURL": os.environ.get("XAI_API_BASE", "https://api.x.ai/v1"),
                        "apiKey": "{env:XAI_API_KEY}",
                    },
                    "models": {
                        "grok-4-1-fast-reasoning": {
                            "name": "Grok 4.1 Fast Reasoning",
                        }
                    },
                }
            },
        }
    if model_id in {"nova-pro", "nova-2-lite"}:
        return {
            "$schema": "https://opencode.ai/config.json",
            "provider": {
                "litellm-bedrock": {
                    "npm": "@ai-sdk/openai-compatible",
                    "name": "LiteLLM Bedrock Proxy",
                    "options": {
                        "baseURL": os.environ.get("LITELLM_BEDROCK_API_BASE", "http://127.0.0.1:4000/v1"),
                        "apiKey": os.environ.get("LITELLM_BEDROCK_API_KEY", "dummy"),
                    },
                    "models": {
                        "nova-pro": {
                            "name": "Nova Pro via AWS Bedrock",
                            "tool_call": True,
                            "temperature": True,
                            "limit": {
                                "context": 128000,
                                "output": 8000,
                            },
                        },
                        "nova-2-lite": {
                            "name": "Nova 2 Lite via AWS Bedrock",
                            "tool_call": True,
                            "temperature": True,
                            "limit": {
                                "context": 128000,
                                "output": 8000,
                            },
                        },
                    },
                }
            },
        }
    if model_id == "granite-4.0-h-small":
        return {
            "$schema": "https://opencode.ai/config.json",
            "provider": {
                "litellm-watsonx": {
                    "npm": "@ai-sdk/openai-compatible",
                    "name": "LiteLLM watsonx Proxy",
                    "options": {
                        "baseURL": os.environ.get("LITELLM_WATSONX_API_BASE", "http://127.0.0.1:4001/v1"),
                        "apiKey": os.environ.get("LITELLM_WATSONX_API_KEY", "dummy"),
                    },
                    "models": {
                        "granite-4.0-h-small": {
                            "name": "Granite 4.0 H-Small via IBM watsonx.ai",
                            "tool_call": True,
                            "temperature": True,
                            "limit": {
                                "context": 128000,
                                "output": 8000,
                            },
                        }
                    },
                }
            },
        }
    if model_id == "granite-4.0-h-tiny-local":
        return {
            "$schema": "https://opencode.ai/config.json",
            "provider": {
                "local-mlx-tiny": {
                    "npm": "@ai-sdk/openai-compatible",
                    "name": "Local MLX (granite-4.0-h-tiny via mlx_lm.server)",
                    "options": {
                        "baseURL": os.environ.get("LOCAL_MLX_TINY_API_BASE", "http://127.0.0.1:8801/v1"),
                        # mlx_lm.server ignores the api key but @ai-sdk requires one.
                        "apiKey": os.environ.get("LOCAL_MLX_API_KEY", "dummy"),
                    },
                    "models": {
                        # mlx_lm.server has a magic "default_model" alias that
                        # always resolves to whatever was loaded at startup.
                        # Using it here lets us avoid embedding the absolute
                        # snapshot path inside the OpenCode model id.
                        "default_model": {
                            "name": "Granite 4.0 H-Tiny (local mlx_lm)",
                        }
                    },
                }
            },
        }
    if model_id == "granite-4.0-h-small-local":
        return {
            "$schema": "https://opencode.ai/config.json",
            "provider": {
                "local-mlx-small": {
                    "npm": "@ai-sdk/openai-compatible",
                    "name": "Local MLX (granite-4.0-h-small mixed-3/4 via mlx_lm.server)",
                    "options": {
                        "baseURL": os.environ.get("LOCAL_MLX_SMALL_API_BASE", "http://127.0.0.1:8802/v1"),
                        "apiKey": os.environ.get("LOCAL_MLX_API_KEY", "dummy"),
                    },
                    "models": {
                        "default_model": {
                            "name": "Granite 4.0 H-Small (local mlx_lm, mixed-3/4-bit)",
                        }
                    },
                }
            },
        }
    return None


def _opencode_variant_request(model_config, sampling):
    by_model = sampling.get("opencode_variant_by_model") or {}
    model_id = model_config.get("id")
    if model_id in by_model:
        return by_model[model_id], "model_override"
    value = sampling.get("opencode_variant")
    if value is None:
        return None, "provider_default"
    return value, "explicit"


def _opencode_variant_sent_to_opencode(model_config, sampling):
    requested, source = _opencode_variant_request(model_config, sampling)
    if requested is None:
        return None, source

    policy = sampling.get("opencode_variant_policy", "supported_only")
    if policy == "all":
        return requested, source

    supported = OPENCODE_VARIANT_SUPPORTED_BY_MODEL.get(model_config.get("id"), set())
    if requested in supported:
        return requested, source

    return None, f"skipped_unsupported_{policy}"


def _sampling_has_explicit_controls(sampling):
    return any(sampling.get(k) is not None for k in ("temperature", "max_tokens", "top_p", "opencode_variant")) or bool(
        sampling.get("opencode_variant_by_model")
    )


def _format_mapping_banner(mapping):
    return f"{len(mapping)} model(s)" if mapping else "None (OpenCode/provider default)"


def build_agentic_sampling_record(model_config, sampling):
    sampling = sampling or {}
    fixed_temp_models = model_config.get("fixed_temperature_only", False)
    provider_family = model_config.get("provider_family")
    opencode_variant_requested, opencode_variant_source = _opencode_variant_request(model_config, sampling)
    opencode_variant_sent, opencode_variant_sent_source = _opencode_variant_sent_to_opencode(model_config, sampling)

    record = {
        "temperature": sampling.get("temperature"),
        "temperature_source": "explicit" if sampling.get("temperature") is not None else "provider_default",
        "temperature_sent_to_opencode": None,
        "max_tokens": sampling.get("max_tokens"),
        "max_tokens_source": "opencode_model_limit_or_provider_default",
        "top_p": sampling.get("top_p"),
        "top_p_source": "explicit" if sampling.get("top_p") is not None else "provider_default",
        "top_p_sent_to_opencode": None,
        "opencode_variant": opencode_variant_sent,
        "opencode_variant_global": sampling.get("opencode_variant"),
        "opencode_variant_by_model": sampling.get("opencode_variant_by_model") or {},
        "opencode_variant_policy": sampling.get("opencode_variant_policy", "supported_only"),
        "opencode_variant_requested": opencode_variant_requested,
        "opencode_variant_source": opencode_variant_source,
        "opencode_variant_sent_to_opencode": opencode_variant_sent,
        "opencode_variant_sent_source": opencode_variant_sent_source,
    }

    if sampling.get("temperature") is not None and not fixed_temp_models:
        record["temperature_sent_to_opencode"] = sampling["temperature"]
    if sampling.get("top_p") is not None and not fixed_temp_models:
        if provider_family == "anthropic" and record["temperature_sent_to_opencode"] is not None:
            record["top_p_source"] = "skipped_for_anthropic_temperature"
        else:
            record["top_p_sent_to_opencode"] = sampling["top_p"]

    return record


def build_workspace_config(model_config, opencode_model, system_prompt, sampling=None):
    sampling_record = build_agentic_sampling_record(model_config, sampling)
    agent_config = {
        "description": "Multi-file Python code generation agent",
        "mode": "primary",
        "model": opencode_model,
        "prompt": "{file:./vibench_agent_prompt.md}",
        "permission": {
            "edit": "allow",
            "bash": "allow",
            "webfetch": "allow",
        },
    }
    if sampling_record["temperature_sent_to_opencode"] is not None:
        agent_config["temperature"] = sampling_record["temperature_sent_to_opencode"]
    if sampling_record["top_p_sent_to_opencode"] is not None:
        agent_config["top_p"] = sampling_record["top_p_sent_to_opencode"]

    config = {
        "$schema": "https://opencode.ai/config.json",
        "agent": {
            "vibench": agent_config
        },
    }
    provider_config = build_workspace_provider_config(model_config["id"])
    if provider_config:
        for key, value in provider_config.items():
            if key == "$schema":
                continue
            if isinstance(value, dict) and isinstance(config.get(key), dict):
                config[key].update(value)
            else:
                config[key] = value
    return config


def prepare_opencode_workspace(workspace_dir, model_config, opencode_model, system_prompt, sampling=None):
    agent_prompt = _build_opencode_agent_prompt(system_prompt)
    (workspace_dir / "vibench_agent_prompt.md").write_text(agent_prompt)
    workspace_config = build_workspace_config(model_config, opencode_model, system_prompt, sampling=sampling)
    (workspace_dir / "opencode.json").write_text(json.dumps(workspace_config, indent=2))
    return agent_prompt, workspace_config


def _classify_opencode_provider_error(stderr):
    text = stderr or ""
    lower = text.lower()
    if "quota exceeded" in lower or "billing details" in lower or "insufficient_quota" in lower:
        return {
            "type": "ProviderQuotaExceeded",
            "message": text[:500] or "Provider quota exceeded.",
        }
    if "rate limit" in lower or "rate_limit" in lower or "too many requests" in lower:
        return {
            "type": "ProviderRateLimit",
            "message": text[:500] or "Provider rate limit hit.",
        }
    return None


def run_opencode(task, prompt, workspace_dir, model_config, verbose=False, timeout=300, system_prompt="", system_prompt_path=None, sampling=None):
    """Run OpenCode non-interactively in the given workspace."""
    model_id = model_config["id"]
    opencode_model, identity_mode, identity_note = resolve_opencode_model(model_id)
    agent_prompt, workspace_config = prepare_opencode_workspace(
        workspace_dir,
        model_config,
        opencode_model,
        system_prompt,
        sampling=sampling,
    )
    task_seed_files = _materialize_seed_files(workspace_dir, task or {})
    prompt_text = prompt
    sampling_record = build_agentic_sampling_record(model_config, sampling)
    cmd = ["opencode", "run", "-m", opencode_model, "--agent", "vibench"]
    if sampling_record.get("opencode_variant"):
        cmd.extend(["--variant", sampling_record["opencode_variant"]])
    cmd.append(prompt)
    prompt_artifacts = {
        "prompt_text": prompt_text,
        "prompt_sha256": _sha256_text(prompt_text),
        "system_prompt": system_prompt,
        "system_prompt_sha256": _sha256_text(system_prompt),
        "system_prompt_path": str(system_prompt_path) if system_prompt_path else None,
        "opencode_agent_prompt": agent_prompt,
        "opencode_agent_prompt_sha256": _sha256_text(agent_prompt),
        "opencode_workspace_config": workspace_config,
        "opencode_workspace_config_sha256": _sha256_json(workspace_config),
        "opencode_command": cmd[:-1] + ["<prompt_text>"],
        "sampling": sampling_record,
        "seed_files": task_seed_files,
    }

    # Set up env with mapped API keys
    env = os.environ.copy()
    for our_key, oc_key in OPENCODE_ENV_MAP.items():
        if our_key in env and oc_key not in env:
            env[oc_key] = env[our_key]

    if verbose:
        print(f"    Workspace: {workspace_dir}")
        print(f"    OpenCode model: {opencode_model}")
        if sampling_record.get("opencode_variant"):
            print(f"    OpenCode variant: {sampling_record['opencode_variant']}")
        print(f"    OpenCode agent: vibench")
        print(f"    Identity mode: {identity_mode}")
        if identity_note:
            print(f"    Identity note: {identity_note}")
        print(f"    Prompt length: {len(prompt_text)} chars")
        print(f"    Running OpenCode...", flush=True)

    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            cwd=str(workspace_dir),
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
        elapsed = time.time() - start
        provider_error = _classify_opencode_provider_error(result.stderr)
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "elapsed_seconds": round(elapsed, 2),
            "opencode_model": opencode_model,
            "opencode_agent": "vibench",
            "system_prompt_mode": "opencode_custom_agent",
            "identity_mode": identity_mode,
            "identity_note": identity_note,
            "error": provider_error or (None if result.returncode == 0 else {
                "type": "NonZeroExit",
                "message": result.stderr[:500]
            }),
            **prompt_artifacts,
        }
    except subprocess.TimeoutExpired:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Timeout after {timeout}s",
            "elapsed_seconds": timeout,
            "opencode_model": opencode_model,
            "opencode_agent": "vibench",
            "system_prompt_mode": "opencode_custom_agent",
            "identity_mode": identity_mode,
            "identity_note": identity_note,
            "error": {"type": "Timeout", "message": f"OpenCode did not complete within {timeout}s"},
            **prompt_artifacts,
        }
    except FileNotFoundError:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": "opencode not found",
            "elapsed_seconds": 0,
            "opencode_model": opencode_model,
            "opencode_agent": "vibench",
            "system_prompt_mode": "opencode_custom_agent",
            "identity_mode": identity_mode,
            "identity_note": identity_note,
            "error": {"type": "NotFound", "message": "opencode CLI not found. Install from https://opencode.ai"},
            **prompt_artifacts,
        }


def _save_agentic_output(out_dir, task, model, variant, ci, result, generated_files, workspace, timeout):
    """Save generated files and metadata for one agentic run."""
    out_dir.mkdir(parents=True, exist_ok=True)
    primary = resolve_primary_component(task)
    scored_files = set(task.get("scored_files", []))
    seed_files = result.get("seed_files") or []
    seeded_file_names = {seed.get("file") for seed in seed_files if isinstance(seed, dict) and seed.get("file")}
    files_present = any(content is not None for content in generated_files.values())

    for fname, content in generated_files.items():
        if content is not None:
            (out_dir / fname).write_text(content)

    meta = {
        "task_id": task["task_id"],
        "modality": "agentic",
        "benchmark": task.get("_benchmark", "vibench"),
        "task_mode": task.get("mode"),
        "primary_atomic_scenario": task.get("primary_atomic_scenario"),
        "primary_component_role": primary.get("role") if primary else None,
        "primary_component_file": primary.get("file") if primary else None,
        "task_family": task.get("family"),
        "evidence_id": task.get("evidence_id"),
        "paired_with": task.get("paired_with"),
        "seed_condition_id": task.get("seed_condition_id"),
        "seed_policy": task.get("seed_policy"),
        "seed_anchor_role": task.get("seed_anchor_role"),
        "seed_anchor_provider": task.get("seed_anchor_provider"),
        "seed_anchor_ecosystem": task.get("seed_anchor_ecosystem"),
        "variant": variant,
        "model_id": model["id"],
        "model_litellm_string": model.get("litellm_string"),
        "model_provider": model.get("api_provider"),
        "model_api_key_env": model.get("api_key_env"),
        "model_affiliation": model.get("ecosystem_affiliation") or model.get("cloud_affiliation"),
        "model_affiliation_scope": "ecosystem",
        "model_cloud_affiliation": model.get("cloud_affiliation"),
        "model_direct_provider_affiliation": model.get("direct_provider_affiliation"),
        "model_ecosystem_affiliation": model.get("ecosystem_affiliation") or model.get("cloud_affiliation"),
        "completion_index": ci,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prompt_text": result.get("prompt_text"),
        "prompt_sha256": result.get("prompt_sha256"),
        "system_prompt": result.get("system_prompt"),
        "system_prompt_sha256": result.get("system_prompt_sha256"),
        "system_prompt_path": result.get("system_prompt_path"),
        "opencode_agent_prompt": result.get("opencode_agent_prompt"),
        "opencode_agent_prompt_sha256": result.get("opencode_agent_prompt_sha256"),
        "opencode_workspace_config": result.get("opencode_workspace_config"),
        "opencode_workspace_config_sha256": result.get("opencode_workspace_config_sha256"),
        "opencode_command": result.get("opencode_command"),
        "sampling": result.get("sampling"),
        "option_order_mode": result.get("option_order_mode"),
        "option_order_affiliation": result.get("option_order_affiliation"),
        "seed_files": seed_files,
        "expected_files": task["expected_files"],
        "scored_files": task.get("scored_files", []),
        "context_files": task.get("context_files", []),
        "files_found": {fname: content is not None for fname, content in generated_files.items()},
        "components": [
            {
                **comp,
                "is_primary": bool(primary and comp.get("file") == primary.get("file")),
                "is_scored": _component_is_scored(comp, scored_files),
                "is_seeded": comp.get("file") in seeded_file_names,
            }
            for comp in task["components"]
        ],
        "elapsed_seconds": result["elapsed_seconds"],
        "opencode_model": result.get("opencode_model"),
        "opencode_agent": result.get("opencode_agent"),
        "agentic_system_prompt_mode": result.get("system_prompt_mode"),
        "agentic_identity_mode": result.get("identity_mode", "exact"),
        "agentic_identity_note": result.get("identity_note"),
        "opencode_exit_code": result["exit_code"],
        "opencode_stdout_tail": (result.get("stdout") or "")[-4000:],
        "opencode_stderr_tail": (result.get("stderr") or "")[-4000:],
        "generation_warning": "NoFilesProduced" if (result.get("error") is None and not files_present) else None,
        "error": result["error"] or ({
            "type": "NoFilesProduced",
            "message": "OpenCode exited without an explicit process error, but none of the expected files were generated.",
        } if not files_present else None),
    }
    with open(out_dir / "_meta.json", "w") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    # Cleanup workspace (log but don't fail on cleanup errors)
    try:
        shutil.rmtree(workspace)
    except OSError as e:
        print(f"  WARNING: workspace cleanup failed for {workspace}: {e}")


def collect_files(workspace_dir, expected_files):
    """Collect generated files from the workspace."""
    found = {}
    for fname in expected_files:
        fpath = workspace_dir / fname
        if fpath.exists():
            found[fname] = fpath.read_text()
        else:
            # Search recursively in case agent put files in subdirectory
            matches = list(workspace_dir.rglob(fname))
            if matches:
                found[fname] = matches[0].read_text()
            else:
                found[fname] = None
    return found


DEFAULT_AGENTIC_CONFIG = {
    "type": "agentic",
    "completions": 1,
    "variants": ["free", "informed"],
    "models": "all",
    "tasks": "all",
    "timeout": 300,
    "max_workers": None,
    "sampling": {},
}


def load_config(config_path=None):
    """Load YAML config, starting from defaults and merging run config."""
    config = dict(DEFAULT_AGENTIC_CONFIG)

    if config_path and Path(config_path).exists():
        with open(config_path) as f:
            run_config = yaml.safe_load(f) or {}
        config.update(run_config)
        config["_source"] = {"run_config": str(Path(config_path).resolve())}
    else:
        config["_source"] = {}

    return config


def apply_cli_overrides(config, args):
    """Override config values with CLI flags where provided."""
    overrides = {}
    if args.task:
        parsed_tasks = _parse_id_list(args.task)
        if parsed_tasks == "all":
            config["tasks"] = "all"
            overrides["tasks"] = "all"
        else:
            config["tasks"] = parsed_tasks
            overrides["tasks"] = parsed_tasks
    if args.model:
        config["models"] = [args.model]
        overrides["models"] = [args.model]
    if args.variant and args.variant != "both":
        config["variants"] = [args.variant]
        overrides["variants"] = [args.variant]
    elif args.variant == "both":
        config["variants"] = ["free", "informed"]
    if args.completions is not None:
        config["completions"] = args.completions
        overrides["completions"] = args.completions
    if args.timeout is not None:
        config["timeout"] = args.timeout
        overrides["timeout"] = args.timeout
    if getattr(args, "opencode_variant", None) is not None:
        config.setdefault("sampling", {})["opencode_variant"] = args.opencode_variant
        overrides["opencode_variant"] = args.opencode_variant
    if args.max_consecutive_errors is not None:
        config["max_consecutive_errors"] = args.max_consecutive_errors
        overrides["max_consecutive_errors"] = args.max_consecutive_errors
    if getattr(args, "retry_errors", False):
        config["retry_errors"] = True
        overrides["retry_errors"] = True
    if getattr(args, "retry_empty", False):
        config["retry_empty"] = True
        overrides["retry_empty"] = True
    if getattr(args, "retry_incomplete", False):
        config["retry_incomplete"] = True
        overrides["retry_incomplete"] = True
    if args.seed_condition:
        config["seed_conditions"] = _normalize_seed_condition_request(args.seed_condition)
        overrides["seed_condition"] = args.seed_condition
    if overrides:
        config["_source"]["cli_overrides"] = overrides
    return config


def main():
    parser = argparse.ArgumentParser(
        description="VIBench Agentic Benchmark Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/generation/run_agentic.py --config configs/vibench/agentic/complete/opencode_full_5c.yaml --resume agentic/complete/opencode_full_5c
  python scripts/generation/run_agentic.py --config configs/vibench/agentic/complete/opencode_full_5c.yaml --task S01 --model gemini-2.5-pro --variant free -v
  python scripts/generation/run_agentic.py --config configs/vibench/agentic/complete/opencode_full_5c.yaml --task S19 S20
  python scripts/generation/run_agentic.py --config configs/vibench/agentic/complete/opencode_full_5c.yaml --dry-run
        """,
    )
    parser.add_argument("--config", type=str, default=None,
                        help="Path to YAML run config")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--name", type=str, default=None,
                        help="Custom run name. Names containing '/' are used as stable paths under outputs/runs/.")
    parser.add_argument("--resume", type=str, default=None,
                        help="Resume into an existing run directory (by name or path)")
    parser.add_argument("--verbose", "-v", action="store_true")

    override = parser.add_argument_group("overrides (take precedence over YAML config)")
    override.add_argument("--task", type=str, nargs="+",
                          help="Task suffixes or full task IDs. Supports space-separated or comma-separated values, "
                               "for example --task S19 S20 or --task S19,S20. Use all to run everything.")
    override.add_argument("--model", type=str, help="Model ID from models.json")
    override.add_argument("--variant", choices=["free", "informed", "both"],
                          help="Prompt variant")
    override.add_argument("--completions", type=int, help="Repetitions per task")
    override.add_argument("--timeout", type=int, help="Timeout per task in seconds")
    override.add_argument("--opencode-variant", type=str,
                          help="OpenCode model variant to pass through, e.g. none, low, medium, high")
    override.add_argument("--seed-condition", type=str,
                          help="Seed condition for benchmarks that define seed_conditions: unseeded, seeded, both, or comma-separated IDs")
    override.add_argument("--workers", type=int, help="Max parallel workers (default: one per model)")
    override.add_argument("--sequential", action="store_true",
                          help="Force sequential execution even with multiple models")
    override.add_argument("--max-consecutive-errors", type=int, default=None,
                          help="Stop scheduling new tasks for a model after N consecutive errors. "
                               "0 disables fail-fast.")
    override.add_argument("--retry-errors", action="store_true",
                          help="On resume, regenerate existing agentic runs whose _meta.json has "
                               "a non-empty error field.")
    override.add_argument("--retry-empty", action="store_true",
                          help="On resume, regenerate existing agentic runs with zero expected "
                               "Python files present.")
    override.add_argument("--retry-incomplete", action="store_true",
                          help="On resume, regenerate existing agentic runs missing any expected "
                               "Python file.")

    args = parser.parse_args()

    # Load config: defaults ← YAML ← CLI
    config = load_config(args.config)
    config = apply_cli_overrides(config, args)
    if args.workers is not None:
        config["max_workers"] = args.workers
    benchmark = config.get("benchmark", "vibench")
    provider_scope = config.get("provider_scope")
    if provider_scope is None and _canonical_benchmark_name(benchmark) != "vibench":
        provider_scope = "all_available"
    reference_cards = _load_direct_reference_cards(benchmark, provider_scope=provider_scope)
    system_prompt_file = config.get("system_prompt_file")
    system_prompt_path = _resolve_agentic_system_prompt_path(
        benchmark,
        system_prompt_file=system_prompt_file,
    )
    system_prompt = _load_agentic_system_prompt(
        benchmark,
        system_prompt_file=system_prompt_file,
    )

    env_path = BASE_DIR / "configs" / ".env"
    load_dotenv(env_path, override=True)

    # Resolve tasks
    task_filter = config.get("tasks", "all")
    if task_filter == "all":
        tasks = load_tasks(benchmark=benchmark)
    else:
        tasks = []
        for t in (task_filter if isinstance(task_filter, list) else [task_filter]):
            tasks.extend(load_tasks(t, benchmark=benchmark))

    # Resolve models
    model_filter = config.get("models", "all")
    if model_filter == "all":
        models = load_models(benchmark=benchmark)
    else:
        models = []
        for m in (model_filter if isinstance(model_filter, list) else [model_filter]):
            models.extend(load_models(m, benchmark=benchmark))
    validate_model_env(models, env_path)

    for task in tasks:
        task["_benchmark"] = benchmark
    task_runs, active_seed_conditions = _expand_tasks_for_seed_conditions(
        tasks,
        config.get("seed_conditions"),
    )

    variants = config["variants"]
    n_completions = config["completions"]
    timeout = config.get("timeout", 300)
    sampling = config.get("sampling", {})
    option_order_mode = config.get("option_order_mode", "balanced")
    max_consecutive_errors = int(config.get("max_consecutive_errors") or 0)
    tasks_path, models_path = _benchmark_paths(benchmark)
    if not models_path.exists():
        models_path = BASE_DIR / "benchmark" / "models.json"

    total = len(task_runs) * len(models) * len(variants) * n_completions

    print("=" * 60)
    print("VIBench Agentic Benchmark")
    print("=" * 60)
    print(f"  Benchmark:   {benchmark}")
    if provider_scope is not None:
        print(f"  Provider scope: {provider_scope}")
    print(f"  Tasks file:  {tasks_path}")
    print(f"  Models file: {models_path}")
    print(f"  Tasks:       {len(tasks)} — {[t['task_id'] for t in tasks]}")
    if active_seed_conditions:
        print(f"  Seed conds:  {active_seed_conditions}")
        print(f"  Task cells:  {len(task_runs)}")
    print(f"  Models:      {len(models)} — {[m['id'] for m in models]}")
    print(f"  Variants:    {variants}")
    print(f"  Completions: {n_completions}")
    print(f"  Timeout:     {timeout}s per task")
    print(f"  System:      {system_prompt_path}")
    print(f"  Option order:{option_order_mode}")
    sampling_mode = (
        "controlled"
        if _sampling_has_explicit_controls(sampling)
        else "provider_default"
    )
    print(
        "  Sampling:    "
        f"temp={_format_sampling_banner(sampling.get('temperature'))}, "
        f"max_tokens={_format_sampling_banner(sampling.get('max_tokens'), 'OpenCode/provider default')}, "
        f"top_p={_format_sampling_banner(sampling.get('top_p'))}, "
        f"opencode_variant={_format_sampling_banner(sampling.get('opencode_variant'), 'OpenCode/provider default')}, "
        f"variant_by_model={_format_mapping_banner(sampling.get('opencode_variant_by_model') or {})}, "
        f"variant_policy={sampling.get('opencode_variant_policy', 'supported_only')} "
        f"[mode={sampling_mode}]"
    )
    if max_consecutive_errors > 0:
        print(f"  Fail-fast:   {max_consecutive_errors} consecutive errors per model")
    print(f"  Total runs:  {total}")
    if len(models) > 1:
        max_workers = config.get("max_workers") or len(models)
        n_workers = min(max_workers, len(models))
        print(f"  Workers:     {n_workers} max")
    print(f"  Env file:    {env_path}")
    print("  Credentials:")
    for model in models:
        required = ", ".join(required_env_vars_for_model(model))
        print(f"    - {model['id']}: {required}")
    if config.get("_source", {}).get("run_config"):
        print(f"  Config:      {config['_source']['run_config']}")
    print()

    if args.dry_run:
        print("DRY RUN:\n")
        for task in task_runs:
            for model in models:
                for variant in variants:
                    for ci in range(1, n_completions + 1):
                        condition = task.get("_seed_condition_id")
                        condition_part = f" × {condition}" if condition else ""
                        print(f"  {task['task_id']} × {model['id']} × {variant}{condition_part} × c{ci}")
                        print(f"    Files: {task['expected_files']}")
        return

    # Create or resume run directory. Searches absolute path first, then
    # results/ and outputs/runs/ recursively, allowing exact relative paths,
    # leaf names, and substring matches.
    if args.resume:
        resume_path = _resolve_existing_run(args.resume)
        if resume_path is None:
            print(f"Cannot find run to resume: {args.resume}  "
                  f"(searched results/ and outputs/runs/)")
            return
        run_dir = resume_path
        try:
            run_name = run_dir.relative_to(RUNS_DIR).as_posix()
        except ValueError:
            run_name = run_dir.name
        print(f"  RESUMING into: {run_dir}")
    else:
        name_suffix = args.name or config.get("name", "agentic")
        if "/" in name_suffix or "\\" in name_suffix:
            run_name = name_suffix
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            run_name = f"{timestamp}_{name_suffix}"
        run_dir = RUNS_DIR / run_name
        run_dir.mkdir(parents=True, exist_ok=True)

    # Save effective config
    config_to_save = {k: v for k, v in config.items() if not k.startswith("_")}
    config_to_save["_meta"] = config.get("_source", {})
    with open(run_dir / "config.yaml", "w") as f:
        yaml.dump(config_to_save, f, default_flow_style=False, sort_keys=False)

    print(f"  Run directory: {run_dir}\n")

    proxy_models = []
    for model in models:
        _, identity_mode, identity_note = resolve_opencode_model(model["id"])
        if identity_mode != "exact":
            proxy_models.append(f"{model['id']} ({identity_note})")
    if proxy_models:
        print("  Agentic identity caveats:")
        for entry in proxy_models:
            print(f"    - {entry}")
        print()

    # Build jobs grouped by model (matching direct runner semantics)
    model_jobs = {}
    jobs = []
    for model in models:
        model_jobs[model["id"]] = []
        for task in task_runs:
            for variant in variants:
                for ci in range(1, n_completions + 1):
                    job = (task, model, variant, ci)
                    model_jobs[model["id"]].append(job)
                    jobs.append(job)

    completed = 0
    skipped = 0
    errors = 0
    aborted = 0
    consecutive_errors = {}
    aborted_models = set()
    start_time = time.time()
    lock = threading.Lock()
    verbose = args.verbose
    retry_errors = bool(config.get("retry_errors"))
    retry_empty = bool(config.get("retry_empty"))
    retry_incomplete = bool(config.get("retry_incomplete"))

    def _agentic_run_needs_retry(out_dir, task):
        """Return True when an existing agentic output should be regenerated."""
        if not (retry_errors or retry_empty or retry_incomplete):
            return False

        meta_path = out_dir / "_meta.json"
        try:
            with open(meta_path) as fh:
                meta = json.load(fh)
        except (OSError, json.JSONDecodeError):
            return True

        if retry_errors and meta.get("error"):
            return True

        expected_files = set(task.get("expected_files") or [])
        actual_present = {path.name for path in out_dir.glob("*.py")}
        meta_files_found = meta.get("files_found")
        if isinstance(meta_files_found, dict):
            meta_present = {name for name, present in meta_files_found.items() if present}
        else:
            meta_present = actual_present
        present = actual_present & meta_present if actual_present else set()

        if retry_empty and not (present & expected_files):
            return True
        if retry_incomplete and expected_files - present:
            return True
        return False

    def _record_model_result(model_id, has_error):
        nonlocal aborted_models
        if max_consecutive_errors <= 0:
            return
        if has_error:
            n = consecutive_errors.get(model_id, 0) + 1
            consecutive_errors[model_id] = n
            if n >= max_consecutive_errors and model_id not in aborted_models:
                aborted_models.add(model_id)
                tqdm.write(
                    f"  ABORT  {model_id}: {n} consecutive errors — "
                    f"skipping remaining tasks for this model "
                    f"(--max-consecutive-errors={max_consecutive_errors})"
                )
        else:
            consecutive_errors[model_id] = 0

    pending_model_jobs = {model_id: [] for model_id in model_jobs}
    pre_skipped = 0
    for model_id, jobs_for_model in model_jobs.items():
        for task, model, variant, ci in jobs_for_model:
            out_id = _agentic_output_id(task, variant, ci)
            out_dir = run_dir / "raw" / "agentic" / model["id"] / out_id
            if out_dir.exists() and (out_dir / "_meta.json").exists():
                if not _agentic_run_needs_retry(out_dir, task):
                    pre_skipped += 1
                    continue
            pending_model_jobs[model_id].append((task, model, variant, ci))

    pending_jobs = [job for jobs_for_model in pending_model_jobs.values() for job in jobs_for_model]
    skipped = pre_skipped

    print(f"  Scheduled:   {len(pending_jobs)} run(s)")
    if pre_skipped:
        print(f"  Pre-skipped: {pre_skipped} existing run(s)")
    print()

    if not pending_jobs:
        duration = time.time() - start_time
        readme = [
            f"# VIBench Agentic Run: {run_name}",
            f"",
            f"**Date**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"**Tasks**: {len(tasks)} — {[t['task_id'] for t in tasks]}",
            f"**Seed conditions**: {active_seed_conditions if active_seed_conditions else []}",
            f"**Task cells**: {len(task_runs)}",
            f"**Models**: {len(models)} — {[m['id'] for m in models]}",
            f"**Variants**: {variants}",
            f"**Completions**: {n_completions}",
            f"**Sampling**: temp={_format_sampling_banner(sampling.get('temperature'))}, max_tokens={_format_sampling_banner(sampling.get('max_tokens'), 'OpenCode/provider default')}, top_p={_format_sampling_banner(sampling.get('top_p'))}, opencode_variant={_format_sampling_banner(sampling.get('opencode_variant'), 'OpenCode/provider default')}, variant_by_model={_format_mapping_banner(sampling.get('opencode_variant_by_model') or {})}, variant_policy={sampling.get('opencode_variant_policy', 'supported_only')} [mode={sampling_mode}]",
            f"**Scheduled**: 0",
            f"**Completed**: {completed}, Skipped: {skipped}, Errors: {errors}, Aborted: {aborted}",
            f"**Max consecutive errors**: {max_consecutive_errors}",
            f"**Fail-fast models**: {sorted(aborted_models) if aborted_models else []}",
            f"**Duration**: {duration:.1f}s",
            f"",
            f"## Identity Notes",
            f"",
            f"Agentic runs preserve the requested model ID in metadata, but some OpenCode routes use proxy backends when an exact native route is unavailable.",
            f"",
            f"## Output Structure",
            f"",
            f"```",
            f"raw/agentic/{{model_id}}/{{task_id}}__{{variant}}__c{{N}}/",
            f"raw/agentic/{{model_id}}/{{task_id}}__{{variant}}__{{seed_condition}}__c{{N}}/  # when seed conditions are explicit",
            f"├── component_a.py       ← generated by the agent",
            f"├── component_b.py",
            f"├── ...",
            f"└── _meta.json           ← run metadata",
            f"```",
        ]
        (run_dir / "README.md").write_text("\n".join(readme))
        print("=" * 60)
        print(f"Done. Completed: {completed}, Skipped: {skipped}, Errors: {errors}, Aborted: {aborted}")
        print(f"Duration: {duration:.1f}s")
        print(f"Run directory: {run_dir}")
        print("=" * 60)
        return

    def _run_job(task, model, variant, ci):
        nonlocal completed, skipped, errors, aborted
        out_id = _agentic_output_id(task, variant, ci)
        out_dir = run_dir / "raw" / "agentic" / model["id"] / out_id

        if out_dir.exists() and (out_dir / "_meta.json").exists():
            if not _agentic_run_needs_retry(out_dir, task):
                with lock:
                    skipped += 1
                return {
                    "status": "skipped",
                    "task": task,
                    "model": model,
                    "variant": variant,
                    "seed_condition_id": task.get("_seed_condition_id"),
                    "completion_index": ci,
                    "files_found": None,
                    "error": None,
                }
            shutil.rmtree(out_dir)

        if model["id"] in aborted_models:
            with lock:
                aborted += 1
            return {
                "status": "aborted",
                "task": task,
                "model": model,
                "variant": variant,
                "seed_condition_id": task.get("_seed_condition_id"),
                "completion_index": ci,
                "files_found": None,
                "error": {
                    "type": "FailFastAborted",
                    "message": f"Skipped after {max_consecutive_errors} consecutive errors for {model['id']}.",
                },
            }

        # Include the run name so concurrent ablation runs do not delete each
        # other's workspaces for the same model/task/completion cell.
        workspace = Path(f"/tmp/vibench_agentic/{run_name}/{model['id']}/{out_id}")
        if workspace.exists():
            shutil.rmtree(workspace)
        workspace.mkdir(parents=True)

        prompt = build_agentic_prompt(
            task,
            variant,
            reference_cards,
            system_prompt=system_prompt,
            completion_index=ci,
            option_order_mode=option_order_mode,
            option_order_affiliation=model.get("ecosystem_affiliation"),
        )
        result = run_opencode(
            task,
            prompt,
            workspace,
            model,
            verbose=verbose,
            timeout=timeout,
            system_prompt=system_prompt,
            system_prompt_path=system_prompt_path,
            sampling=sampling,
        )
        result["option_order_mode"] = option_order_mode
        result["option_order_affiliation"] = model.get("ecosystem_affiliation")
        generated_files = collect_files(workspace, task["expected_files"])
        files_found = sum(1 for v in generated_files.values() if v is not None)
        error = result["error"] or ({
            "type": "NoFilesProduced",
            "message": "OpenCode exited without an explicit process error, but none of the expected files were generated.",
        } if files_found == 0 else None)

        with lock:
            completed += 1
            if error:
                errors += 1
            _record_model_result(model["id"], bool(error))

        _save_agentic_output(out_dir, task, model, variant, ci, result, generated_files, workspace, timeout)
        return {
            "status": "ok" if not error else "error",
            "task": task,
            "model": model,
            "variant": variant,
            "seed_condition_id": task.get("_seed_condition_id"),
            "completion_index": ci,
            "files_found": files_found,
            "error": error,
            "elapsed_seconds": result["elapsed_seconds"],
        }

    def _process_model_jobs(model_id, jobs_for_model, pbar=None):
        for task, model, variant, ci in jobs_for_model:
            result = _run_job(task, model, variant, ci)

            if pbar:
                if result["status"] == "skipped":
                    pbar.update(1)
                    continue
                pbar.set_postfix_str(
                    f"{_agentic_job_label(task, variant, ci)}|{result['files_found']}/{len(task['expected_files'])}|err={errors}"
                )
                pbar.update(1)

            if verbose:
                tag = f"[{completed + skipped + aborted}/{len(jobs)}]"
                label = f"{task['task_id']} × {model['id']} × {variant}"
                if task.get("_seed_condition_id"):
                    label += f" × {task['_seed_condition_id']}"
                label += f" × c{ci}"
                if result["status"] == "skipped":
                    print(f"{tag} {label} ... SKIP")
                elif result["status"] == "aborted":
                    print(f"{tag} {label} ... ABORTED")
                elif result["error"]:
                    print(f"{tag} {label} ... "
                          f"ERROR: {result['error']['type']}: {result['error']['message'][:60]}")
                else:
                    print(f"{tag} {label} ... "
                          f"OK ({result['elapsed_seconds']}s) | {result['files_found']}/{len(task['expected_files'])} files")

    if verbose:
        # Verbose: sequential per-call output
        for model_id, jobs_for_model in pending_model_jobs.items():
            _process_model_jobs(model_id, jobs_for_model, pbar=None)
    else:
        max_workers = config.get("max_workers") or len(models)
        parallel = len(models) > 1 and not getattr(args, 'sequential', False)
        active_model_ids = [model_id for model_id, jobs_for_model in pending_model_jobs.items() if jobs_for_model]
        n_workers = min(max_workers, len(active_model_ids)) if parallel else 1

        if parallel:
            print(f"  Parallel: {n_workers} workers for {len(active_model_ids)} active model(s)\n")

            pbar_total = tqdm(
                total=len(pending_jobs), desc="Total", position=0, unit="call",
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
            )
            model_pbars = {}
            for idx, model_id in enumerate(active_model_ids, start=1):
                n_model_jobs = len(pending_model_jobs[model_id])
                model_pbars[model_id] = tqdm(
                    total=n_model_jobs, desc=f"  {model_id[:28]:28s}", position=idx, unit="call",
                    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}]",
                    leave=False,
                )

            def _parallel_process(model_id, jobs_for_model):
                model_pbar = model_pbars[model_id]
                for task, model, variant, ci in jobs_for_model:
                    result = _run_job(task, model, variant, ci)
                    model_pbar.update(1)
                    pbar_total.update(1)
                    if result["status"] != "skipped":
                        model_pbar.set_postfix_str(
                            f"{_agentic_job_label(task, variant, ci)}|{result['files_found']}/{len(task['expected_files'])}|err={errors}"
                        )

            with ThreadPoolExecutor(max_workers=n_workers) as executor:
                futures = {}
                for model_id in active_model_ids:
                    jobs_for_model = pending_model_jobs[model_id]
                    future = executor.submit(_parallel_process, model_id, jobs_for_model)
                    futures[future] = model_id

                for future in as_completed(futures):
                    model_id = futures[future]
                    try:
                        future.result()
                    except Exception as e:
                        print(f"\n  THREAD ERROR ({model_id}): {e}")

            for pb in model_pbars.values():
                pb.close()
            pbar_total.close()
        else:
            pbar = tqdm(total=len(pending_jobs), desc="Total", unit="call")
            for model_id, jobs_for_model in pending_model_jobs.items():
                _process_model_jobs(model_id, jobs_for_model, pbar)
            pbar.close()

    duration = time.time() - start_time

    # Write README
    readme = [
        f"# VIBench Agentic Run: {run_name}",
        f"",
        f"**Date**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"**Tasks**: {len(tasks)} — {[t['task_id'] for t in tasks]}",
        f"**Seed conditions**: {active_seed_conditions if active_seed_conditions else []}",
        f"**Task cells**: {len(task_runs)}",
        f"**Models**: {len(models)} — {[m['id'] for m in models]}",
        f"**Variants**: {variants}",
        f"**Completions**: {n_completions}",
        f"**Sampling**: temp={_format_sampling_banner(sampling.get('temperature'))}, max_tokens={_format_sampling_banner(sampling.get('max_tokens'), 'OpenCode/provider default')}, top_p={_format_sampling_banner(sampling.get('top_p'))}, opencode_variant={_format_sampling_banner(sampling.get('opencode_variant'), 'OpenCode/provider default')}, variant_by_model={_format_mapping_banner(sampling.get('opencode_variant_by_model') or {})}, variant_policy={sampling.get('opencode_variant_policy', 'supported_only')} [mode={sampling_mode}]",
        f"**Scheduled**: {len(pending_jobs)}",
        f"**Completed**: {completed}, Skipped: {skipped}, Errors: {errors}, Aborted: {aborted}",
        f"**Max consecutive errors**: {max_consecutive_errors}",
        f"**Fail-fast models**: {sorted(aborted_models) if aborted_models else []}",
        f"**Duration**: {duration:.1f}s",
        f"",
        f"## Identity Notes",
        f"",
        f"Agentic runs preserve the requested model ID in metadata, but some OpenCode routes use proxy backends when an exact native route is unavailable.",
        f"",
        f"## Output Structure",
        f"",
        f"```",
        f"raw/agentic/{{model_id}}/{{task_id}}__{{variant}}__c{{N}}/",
        f"raw/agentic/{{model_id}}/{{task_id}}__{{variant}}__{{seed_condition}}__c{{N}}/  # when seed conditions are explicit",
        f"├── component_a.py       ← generated by the agent",
        f"├── component_b.py",
        f"├── ...",
        f"└── _meta.json           ← run metadata",
        f"```",
    ]
    (run_dir / "README.md").write_text("\n".join(readme))

    print()
    print("=" * 60)
    print(f"Done. Completed: {completed}, Skipped: {skipped}, Errors: {errors}, Aborted: {aborted}")
    if aborted_models:
        print(f"Fail-fast hit: {', '.join(sorted(aborted_models))}")
    print(f"Duration: {duration:.1f}s")
    if len(models) > 1:
        mode = "sequential" if verbose or getattr(args, 'sequential', False) else "parallel"
        print(f"Mode: {mode} ({len(models)} models)")
    print(f"Run directory: {run_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
