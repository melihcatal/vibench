"""
VIBench Pilot Study — Execution Script
Runs pilot prompts across models via LiteLLM.

Each run creates a folder under outputs/runs/ containing:
  - config.yaml     — the full effective config (YAML + CLI overrides merged)
  - README.md       — auto-generated experiment description
  - raw/{modality}/ — one JSON file per completion

Usage:
    python scripts/generation/run_direct.py --config configs/vibench/direct/complete/full_5c.yaml --resume direct/complete/full_5c
    python scripts/generation/run_direct.py --config configs/vibench/direct/complete/full_5c.yaml --model gemini-2.5-flash --scenario S05
    python scripts/generation/run_direct.py --config configs/vibench/direct/complete/full_5c.yaml --dry-run
"""

import json
import hashlib
import os
import re
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime, timezone

import yaml
import litellm
litellm.drop_params = True  # Drop unsupported params per provider instead of erroring
litellm.suppress_debug_info = True  # Suppress "Provider List" and "Give Feedback" stderr messages
from dotenv import load_dotenv
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / "configs" / "default.yaml"
RUNS_DIR = BASE_DIR.parent / "outputs" / "runs"
RUN_SEARCH_DIRS = [RUNS_DIR]
OPEN_REFERENCE_MODALITY = "reference_open"
LEGACY_CS_MODALITY = "cs_documented"
REFERENCE_MODALITY_ALIASES = {OPEN_REFERENCE_MODALITY, LEGACY_CS_MODALITY}


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


def resolve_existing_run(run_id):
    candidate = Path(run_id)
    if candidate.exists() and candidate.is_dir():
        return candidate.resolve()
    for base in RUN_SEARCH_DIRS:
        candidate = base / run_id
        if candidate.exists() and candidate.is_dir():
            return candidate
    for base in RUN_SEARCH_DIRS:
        for run_path in _iter_run_dirs(base):
            rel = _run_match_key(base, run_path)
            if run_path.name == run_id or rel == run_id:
                return run_path
    for base in RUN_SEARCH_DIRS:
        matches = sorted([
            d for d in _iter_run_dirs(base)
            if run_id in d.name or run_id in _run_match_key(base, d)
        ])
        if matches:
            return matches[-1]
    return None
BENCHMARK_ALIASES = {
    "vibench": "vibench",
    "current": "vibench",
    "v3": "vibench",
    "v3_core4": "vibench",
}


def _is_reference_modality(modality):
    return modality in REFERENCE_MODALITY_ALIASES


def _reference_task_id(subtask, canonical_modality=OPEN_REFERENCE_MODALITY):
    direct_ids = subtask.get("direct_task_ids") or {}
    return (
        direct_ids.get(canonical_modality)
        or direct_ids.get(LEGACY_CS_MODALITY)
        or direct_ids.get("cs")
    )


def _canonical_benchmark_name(benchmark):
    key = (benchmark or "vibench").strip().lower()
    if key not in BENCHMARK_ALIASES:
        raise ValueError(f"Unsupported benchmark '{benchmark}'. This repository keeps only the current 'vibench' benchmark.")
    return BENCHMARK_ALIASES[key]


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


def load_config(config_path=None):
    """Load YAML config, starting from default and merging the run config."""
    with open(DEFAULT_CONFIG_PATH) as f:
        config = yaml.safe_load(f)

    config["_source"] = {"default": str(DEFAULT_CONFIG_PATH)}

    if config_path and Path(config_path).exists():
        with open(config_path) as f:
            run_config = yaml.safe_load(f) or {}
        for key, value in run_config.items():
            if isinstance(value, dict) and key in config and isinstance(config[key], dict):
                config[key].update(value)
            else:
                config[key] = value
        config["_source"]["run_config"] = str(Path(config_path).resolve())

    return config


def apply_cli_overrides(config, args):
    """Override config values with CLI flags where provided."""
    overrides = {}
    if getattr(args, "benchmark", None):
        config["benchmark"] = args.benchmark
        overrides["benchmark"] = args.benchmark
    if args.completions is not None:
        config["completions"] = args.completions
        overrides["completions"] = args.completions
    if args.model:
        # nargs="+" so args.model is always a list
        config["models"] = list(args.model)
        overrides["models"] = list(args.model)
    if args.scenario:
        parsed_scenarios = _parse_id_list(args.scenario)
        config["scenarios"] = parsed_scenarios
        overrides["scenarios"] = parsed_scenarios
    if args.modality:
        config["modalities"] = [args.modality]
        overrides["modalities"] = [args.modality]
    if getattr(args, "limit", None):
        config["limit_per_model"] = args.limit
        overrides["limit_per_model"] = args.limit
    if args.temperature is not None:
        config["sampling"]["temperature"] = args.temperature
        overrides["temperature"] = args.temperature
    if args.max_tokens is not None:
        config["sampling"]["max_tokens"] = args.max_tokens
        overrides["max_tokens"] = args.max_tokens
    if getattr(args, "reasoning_effort", None) is not None:
        config["sampling"]["reasoning_effort"] = args.reasoning_effort
        overrides["reasoning_effort"] = args.reasoning_effort
    if getattr(args, "rate_limit_delay", None) is not None:
        # nargs="+" so this is a list of floats, possibly length 1.
        delays = list(args.rate_limit_delay)
        if len(delays) == 1:
            # Single value: broadcast to every model.
            config["rate_limit_delay"] = delays[0]
            overrides["rate_limit_delay"] = delays[0]
        else:
            # Multiple values: must align with --model.
            cli_models = list(args.model) if args.model else []
            if not cli_models:
                raise SystemExit(
                    f"--rate-limit-delay was given {len(delays)} values but no "
                    f"--model list to match them against. Pass --model "
                    f"<id1> <id2> ... in the same order, or pass a single delay."
                )
            if len(delays) != len(cli_models):
                raise SystemExit(
                    f"--rate-limit-delay has {len(delays)} values but --model has "
                    f"{len(cli_models)} ids. They must match positionally, or pass "
                    f"a single delay to broadcast to all models."
                )
            per_model = dict(zip(cli_models, delays))
            config["rate_limit_delay_per_model"] = per_model
            overrides["rate_limit_delay_per_model"] = per_model
    if getattr(args, "skip_from", None) is not None:
        config["skip_from"] = args.skip_from
        overrides["skip_from"] = args.skip_from
    if getattr(args, "retry_errors", False):
        config["retry_errors"] = True
        overrides["retry_errors"] = True
    if getattr(args, "retry_empty", False):
        config["retry_empty"] = True
        overrides["retry_empty"] = True
    if getattr(args, "max_consecutive_errors", None) is not None:
        config["max_consecutive_errors"] = args.max_consecutive_errors
        overrides["max_consecutive_errors"] = args.max_consecutive_errors
    if overrides:
        config["_source"]["cli_overrides"] = overrides
    return config


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def resolve_path(config, key):
    return BASE_DIR / config["paths"][key]


def datasets_dir(config):
    """Return the datasets directory for the active benchmark version."""
    benchmark = _canonical_benchmark_name(config.get("benchmark", "vibench"))
    return BASE_DIR / config["paths"]["datasets"] / benchmark


def load_system_prompt(config):
    return system_prompt_path(config).read_text().strip()


def system_prompt_path(config):
    prompt_file = config.get("system_prompt_file") or config["paths"]["system_prompt"]
    path = Path(prompt_file)
    if path.is_absolute():
        return path
    versioned = datasets_dir(config) / prompt_file
    if versioned.exists():
        return versioned
    return BASE_DIR / prompt_file


def load_models(config):
    with open(datasets_dir(config) / config["paths"]["models_file"]) as f:
        all_models = json.load(f)["models"]
    if config["models"] == "all":
        return all_models
    return [m for m in all_models if m["id"] in config["models"]]


EXTRA_REQUIRED_ENV = {
    "ibm": ["WATSONX_PROJECT_ID", "WATSONX_URL"],
}
# Bedrock models need AWS creds; Nova API models just need AMAZON_NOVA_API_KEY
BEDROCK_EXTRA_ENV = ["AWS_SECRET_ACCESS_KEY", "AWS_REGION_NAME"]


def required_env_vars_for_model(model):
    required = []
    base_env = model.get("api_base_env")
    if base_env:
        required.append(base_env)
    primary = model.get("api_key_env")
    if primary:
        required.append(primary)
    # Bedrock models need extra AWS creds; Nova API models don't
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


def load_scenario_files(config, modality):
    if _uses_hf_direct_dataset(config):
        return load_hf_direct_scenarios(config, modality)

    folder = datasets_dir(config) / modality
    if _is_reference_modality(modality) and not folder.exists():
        # Legacy v1/v2 direct datasets store this modality under cs_documented.
        folder = datasets_dir(config) / LEGACY_CS_MODALITY
    scenarios = []
    for f in sorted(folder.glob("*.json")):
        with open(f) as fh:
            data = json.load(fh)
        if config["scenarios"] != "all":
            if data["scenario_id"] not in config["scenarios"]:
                continue
        data.setdefault("modality", modality)
        scenarios.append(data)
    return scenarios


def _uses_hf_direct_dataset(config):
    dataset_file = config.get("dataset_file")
    if dataset_file:
        return True
    return (datasets_dir(config) / "direct" / "tasks.jsonl").exists()


def _provider_scope(config):
    benchmark = _canonical_benchmark_name(config.get("benchmark", ""))
    if "provider_scope" in config:
        return config.get("provider_scope")
    if benchmark == "vibench":
        return None
    return "all_available"


def _provider_scope_allowed(scope):
    if scope == "core4":
        return {"aws", "google", "microsoft_openai", "alibaba"}
    if scope in {"all5", "all5_eligible"}:
        return {"aws", "google", "microsoft_openai", "alibaba", "ibm"}
    return None


def _hf_direct_dataset_path(config):
    if config.get("dataset_file"):
        path = Path(config["dataset_file"])
        return path if path.is_absolute() else BASE_DIR / path
    return datasets_dir(config) / "direct" / "tasks.jsonl"


def _load_hf_direct_rows(config):
    path = _hf_direct_dataset_path(config)
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if config["scenarios"] != "all":
        wanted = set(config["scenarios"])
        rows = [row for row in rows if row["scenario_id"] in wanted]

    scope = _provider_scope(config)
    if scope in {"all5", "all5_eligible"}:
        rows = [row for row in rows if row.get("coverage", {}).get("all5")]
    return rows


def _hf_provider_tools_to_options(row, config):
    scope = _provider_scope(config)
    allowed = _provider_scope_allowed(scope)
    options = {}
    provider_tools = list(row["provider_tools"])
    if scope is None:
        provider_tools.extend(row.get("neutral_tools") or [])
    for tool in provider_tools:
        provider_key = tool["provider_key"]
        if allowed is not None and provider_key not in allowed:
            continue
        if not tool.get("eligible", True):
            continue
        docs = [doc["url"] for doc in tool.get("official_docs", []) if doc.get("url")]
        options[provider_key] = {
            "label": tool.get("label") or tool.get("service") or provider_key,
            "service": tool.get("service") or tool.get("label") or provider_key,
            "sdk": tool.get("sdk") or "unknown",
            "interface": tool.get("interface"),
            "operations": tool.get("operations") or [],
            "setup_hints": tool.get("auth_env") or [],
            "evidence_ref": {
                "docs": docs,
                "notes": tool.get("notes"),
            },
        }
    return options


def load_hf_direct_scenarios(config, modality):
    """Adapt vibench HuggingFace-style rows into the existing per-modality shape."""
    scenarios = []
    for row in _load_hf_direct_rows(config):
        context = {
            "scenario_id": row["scenario_id"],
            "title": row["title"],
            "class": row.get("family"),
            "task_description": row.get("task_description") or row.get("title"),
            "dataset_kind": row.get("dataset_kind"),
            "coverage": row.get("coverage"),
            "notes": row.get("notes"),
            "competition": row.get("competition"),
            "_hf_row": row,
        }
        if modality == "nli":
            sub_requirements = [
                {
                    "id": st["direct_task_ids"]["nli"],
                    "description": st.get("description"),
                    "prompt": st["nli_prompt"],
                }
                for st in row["subtasks"]
            ]
            scenarios.append({**context, "modality": "nli", "sub_requirements": sub_requirements})
        elif modality == "fim":
            sub_requirements = [
                {
                    "id": st["direct_task_ids"]["fim"],
                    "description": st.get("description"),
                    "instruction": st["fim_instruction"],
                    "skeleton": st["fim_skeleton"],
                }
                for st in row["subtasks"]
            ]
            scenarios.append({**context, "modality": "fim", "sub_requirements": sub_requirements})
        elif _is_reference_modality(modality):
            options = _hf_provider_tools_to_options(row, config)
            sub_requirements = [
                {
                    "id": _reference_task_id(st, modality),
                    "description": st.get("description"),
                    "task_prompt": st.get("reference_open_task_prompt") or st["cs_task_prompt"],
                }
                for st in row["subtasks"]
            ]
            missing_ids = [st.get("subtask_id", st.get("role", "?")) for st, sr in zip(row["subtasks"], sub_requirements) if not sr["id"]]
            if missing_ids:
                raise ValueError(
                    f"Missing documented-reference task ids for {row['scenario_id']}: {', '.join(missing_ids)}"
                )
            scenarios.append({
                **context,
                "modality": modality,
                "render_style": "reference_card",
                "instruction_reference": (
                    "The following documented provider tools are reference options known to fit "
                    "this task. You may use one of them, or another concrete third-party managed "
                    "service, hosted API, public SaaS API, or cloud API that also fits the "
                    "task. The option order is arbitrary and not a ranking. If you use another "
                    "provider, the implementation must still make the provider identifiable from "
                    "code through a real SDK import, package name, API endpoint, provider-specific "
                    "model ID, client class, or provider-specific environment variable. "
                    "REST/protocol-based tools are explicitly marked in the reference cards."
                ),
                "options": options,
                "uniform_baseline": round(1 / len(options), 6) if options else None,
                "sub_requirements": sub_requirements,
            })
        else:
            raise ValueError(f"Unsupported modality for HF direct dataset: {modality}")
    return scenarios


# ---------------------------------------------------------------------------
# Prompt assembly
# ---------------------------------------------------------------------------

def _scenario_context(scenario):
    return {
        "scenario_id": scenario["scenario_id"],
        "scenario_title": scenario.get("title") or scenario.get("scenario_title"),
        "scenario_class": scenario.get("class") or scenario.get("scenario_class"),
        "scenario_task_description": scenario.get("task_description"),
        "scenario_competition": scenario.get("competition"),
        "scenario_notes": scenario.get("notes"),
        "scenario_coverage": scenario.get("coverage"),
    }


def assemble_nli_prompts(scenario):
    context = _scenario_context(scenario)
    for sr in scenario["sub_requirements"]:
        parts = []
        if context["scenario_task_description"]:
            parts.append(f"Task: {context['scenario_task_description']}")
        parts.append(sr["prompt"])
        yield {
            **context,
            "modality": "nli",
            "task_id": sr["id"],
            "sub_requirement_id": sr["id"],
            "sub_requirement_description": sr.get("description"),
            "prompt_text": "\n\n".join(parts),
        }


def assemble_fim_prompts(scenario):
    context = _scenario_context(scenario)
    for sr in scenario["sub_requirements"]:
        parts = []
        if context["scenario_task_description"]:
            parts.append(f"Task: {context['scenario_task_description']}")
        parts.append(sr["instruction"])
        parts.append(sr["skeleton"])
        yield {
            **context,
            "modality": "fim",
            "task_id": sr["id"],
            "sub_requirement_id": sr["id"],
            "sub_requirement_description": sr.get("description"),
            "prompt_text": "\n\n".join(parts),
        }


def _seeded_shuffle(items, seed_str):
    """Deterministic shuffle using a string seed."""
    import hashlib
    seed_int = int(hashlib.sha256(seed_str.encode()).hexdigest()[:8], 16)
    rng = __import__("random").Random(seed_int)
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


def _extract_env_var_names(text):
    envs = []
    patterns = [
        r"os\.environ\['([^']+)'\]",
        r'os\.environ\["([^"]+)"\]',
        r"os\.getenv\('([^']+)'",
        r'os\.getenv\("([^"]+)"',
    ]
    for pattern in patterns:
        envs.extend(re.findall(pattern, text))

    unique = []
    for env in envs:
        if env not in unique:
            unique.append(env)
    return unique


def _extract_operation_names(text):
    ignore = {
        "open", "read", "write", "print", "append", "extend", "result", "json",
        "get", "post", "put", "list", "call", "create", "client", "init",
    }
    names = []
    for name in re.findall(r"\.([A-Za-z_][A-Za-z0-9_]*)\(", text):
        if name.lower() in ignore:
            continue
        if name not in names:
            names.append(name)
    return names[:4]


def _build_reference_card(opt):
    lines = [
        f"  Service: {opt.get('service', opt['label'])}",
        f"  SDK: {opt.get('sdk', 'unknown')}",
    ]
    if opt.get("interface"):
        lines.append(f"  Interface: {opt['interface']}")

    operations = opt.get("operations") or _extract_operation_names(opt.get("skeleton", ""))
    if operations:
        lines.append(f"  Documented operations: {', '.join(operations[:3])}")
    else:
        lines.append("  Documented operations: see linked official SDK/API methods")

    envs = opt.get("setup_hints") or _extract_env_var_names(opt.get("skeleton", ""))
    if envs:
        lines.append(f"  Setup hints: {', '.join(envs[:3])}")
    else:
        lines.append("  Setup hints: provider credentials and endpoint configuration")

    docs = (opt.get("evidence_ref") or {}).get("docs") or []
    if docs:
        lines.append(f"  Official docs: {', '.join(docs[:2])}")

    return lines


def _materialize_cs_task(
    task,
    completion_index,
    option_order_mode="balanced",
    affiliation=None,
):
    """Build a completion-specific CS prompt with deterministic option ordering."""
    options = task["cs_options"]
    option_keys = list(options.keys())
    seed_str = _provider_option_order_seed(
        task["scenario_id"],
        completion_index,
        option_order_mode=option_order_mode,
        affiliation=affiliation,
    )
    shuffled_keys = _ordered_provider_options(
        option_keys,
        task["scenario_id"],
        completion_index,
        option_order_mode=option_order_mode,
        affiliation=affiliation,
    )

    parts = []
    if task.get("scenario_task_description"):
        parts.append(f"Task: {task['scenario_task_description']}")
        parts.append("")
    if task.get("cs_task_prompt"):
        parts.append(task["cs_task_prompt"])
        parts.append("")
    parts.append(task["cs_instruction"])
    parts.append("")

    option_labels = []
    option_services = []
    render_style = task.get("cs_render_style", "skeleton")

    for i, provider_key in enumerate(shuffled_keys, 1):
        opt = options[provider_key]
        parts.append(f"Option {i} — {opt['label']}:")
        if render_style == "reference_card":
            parts.extend(_build_reference_card(opt))
        else:
            for line in opt["skeleton"].split("\n"):
                parts.append(f"  {line}")
        parts.append("")
        option_labels.append(opt["label"])
        option_services.append(opt.get("service", opt["label"]))

    parts.append(
        "Return exactly one complete implementation. If you use a listed option, adapt its SDK, "
        "REST, or protocol surface. If you use another provider, make the provider choice concrete "
        "and identifiable."
    )

    return {
        **task,
        "cs_option_keys": shuffled_keys,
        "cs_option_labels": option_labels,
        "cs_option_services": option_services,
        "cs_ordering_seed": seed_str,
        "option_order_mode": option_order_mode or "balanced",
        "option_order_affiliation": affiliation,
        "reference_option_keys": shuffled_keys,
        "reference_option_labels": option_labels,
        "reference_option_services": option_services,
        "reference_ordering_seed": seed_str,
        "rotation_size": len(shuffled_keys),
        "prompt_text": "\n".join(parts).strip(),
    }


def assemble_cs_prompts(scenario):
    """Assemble documented reference prompt templates for later materialization."""
    context = _scenario_context(scenario)
    options = scenario["options"]
    benchmark = _canonical_benchmark_name(scenario.get("_benchmark", "vibench"))
    render_style = scenario.get("render_style") or ("reference_card" if benchmark == "legacy" else "skeleton")
    modality = scenario.get("modality") or LEGACY_CS_MODALITY
    if render_style == "reference_card":
        instruction = scenario.get(
            "instruction_reference",
            "The following documented provider tools are reference options known to fit this task. "
            "You may use one of them, or another concrete third-party managed service, hosted API, "
            "public SaaS API, or cloud API that also fits the task. The option order is arbitrary "
            "and not a ranking. Each option shows a provider reference card with service name, SDK, "
            "documented operations, and setup hints."
        )
    else:
        instruction = scenario.get(
            "instruction",
            "The following options are reference implementations known to fit this task. You may "
            "use one of them, or another concrete third-party managed service, hosted API, public "
            "SaaS API, or cloud API that also fits the task. The option order is arbitrary and not "
            "a ranking. Each option shows the SDK and a working code skeleton."
        )

    for sr in scenario.get("sub_requirements", []):
        task = {
            **context,
            "modality": modality,
            "task_id": sr["id"],
            "sub_requirement_id": sr["id"],
            "sub_requirement_description": sr.get("description"),
            "cs_instruction": instruction,
            "cs_task_prompt": sr.get("task_prompt", ""),
            "cs_options": options,
            "cs_render_style": render_style,
            "uniform_baseline": scenario.get("uniform_baseline"),
        }
        yield _materialize_cs_task(task, completion_index=1)


ASSEMBLERS = {
    "nli": assemble_nli_prompts,
    "fim": assemble_fim_prompts,
    OPEN_REFERENCE_MODALITY: assemble_cs_prompts,
    LEGACY_CS_MODALITY: assemble_cs_prompts,
}


# ---------------------------------------------------------------------------
# API calling
# ---------------------------------------------------------------------------

DIRECT_REASONING_EFFORT_SUPPORTED_BY_MODEL = {
    # Verified through LiteLLM/OpenAI route behavior and OpenCode parity needs.
    "gpt-5.4": {"none", "medium"},
    "gpt-5.4-mini": {"none", "medium"},
}


def _reasoning_effort_request(model, sampling):
    by_model = sampling.get("reasoning_effort_by_model") or {}
    model_id = model.get("id")
    if model_id in by_model:
        return by_model[model_id], "model_override"
    value = sampling.get("reasoning_effort")
    if value is None:
        return None, "provider_default"
    return value, "explicit"


def _reasoning_effort_sent_to_api(model, sampling):
    requested, source = _reasoning_effort_request(model, sampling)
    if requested is None:
        return None, source

    policy = sampling.get("reasoning_effort_policy", "supported_only")
    if policy == "all":
        return requested, source

    supported = DIRECT_REASONING_EFFORT_SUPPORTED_BY_MODEL.get(model.get("id"), set())
    if requested in supported:
        return requested, source

    return None, f"skipped_unsupported_{policy}"


def _sampling_has_explicit_controls(sampling):
    return any(sampling.get(k) is not None for k in ("temperature", "max_tokens", "top_p", "reasoning_effort")) or bool(
        sampling.get("reasoning_effort_by_model")
    )


def _format_mapping_banner(mapping):
    return f"{len(mapping)} model(s)" if mapping else "None (provider default)"


def _save_record(filepath, task, model, ci, sampling, result, system_prompt=None, system_prompt_path_value=None):
    """Save a single completion result."""
    # Record what was actually sent to the API vs provider default
    fixed_temp_models = model.get("fixed_temperature_only", False)
    temperature_sent = sampling.get("temperature") if sampling.get("temperature") is not None and not fixed_temp_models else None
    max_tokens_sent = sampling.get("max_tokens") if sampling.get("max_tokens") is not None else None
    top_p_sent = None
    top_p_source = "explicit" if sampling.get("top_p") is not None else "provider_default"
    if sampling.get("top_p") is not None and not fixed_temp_models:
        if "anthropic" in model["litellm_string"] and temperature_sent is not None:
            top_p_source = "skipped_for_anthropic_temperature"
        else:
            top_p_sent = sampling["top_p"]
    reasoning_requested, reasoning_source = _reasoning_effort_request(model, sampling)
    reasoning_sent, reasoning_sent_source = _reasoning_effort_sent_to_api(model, sampling)
    sampling_record = {
        "temperature": sampling.get("temperature"),
        "temperature_source": "explicit" if sampling.get("temperature") is not None else "provider_default",
        "temperature_sent_to_api": temperature_sent,
        "max_tokens": sampling.get("max_tokens"),
        "max_tokens_sent_to_api": max_tokens_sent,
        "top_p": sampling.get("top_p"),
        "top_p_source": top_p_source,
        "top_p_sent_to_api": top_p_sent,
        "reasoning_effort": reasoning_requested,
        "reasoning_effort_global": sampling.get("reasoning_effort"),
        "reasoning_effort_by_model": sampling.get("reasoning_effort_by_model") or {},
        "reasoning_effort_policy": sampling.get("reasoning_effort_policy", "supported_only"),
        "reasoning_effort_requested": reasoning_requested,
        "reasoning_effort_source": reasoning_source,
        "reasoning_effort_sent_to_api": reasoning_sent,
        "reasoning_effort_sent_source": reasoning_sent_source,
    }
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": task.get("prompt_text")},
    ]

    record = {
        "benchmark": task.get("benchmark"),
        "task_id": task["task_id"],
        "modality": task["modality"],
        "model_id": model["id"],
        "model_litellm_string": model["litellm_string"],
        "model_provider": model["api_provider"],
        "model_api_key_env": model.get("api_key_env"),
        "model_affiliation": model.get("ecosystem_affiliation") or model.get("cloud_affiliation"),
        "model_affiliation_scope": "ecosystem",
        "model_cloud_affiliation": model.get("cloud_affiliation"),
        "model_direct_provider_affiliation": model.get("direct_provider_affiliation"),
        "model_ecosystem_affiliation": model.get("ecosystem_affiliation") or model.get("cloud_affiliation"),
        "direct_provider_affiliation": model.get("direct_provider_affiliation"),
        "provider_family": model.get("provider_family"),
        "ecosystem_affiliation": model.get("ecosystem_affiliation") or model.get("cloud_affiliation"),
        "scenario_id": task.get("scenario_id"),
        "scenario_title": task.get("scenario_title"),
        "scenario_class": task.get("scenario_class"),
        "scenario_task_description": task.get("scenario_task_description"),
        "scenario_competition": task.get("scenario_competition"),
        "scenario_notes": task.get("scenario_notes"),
        "scenario_coverage": task.get("scenario_coverage"),
        "sub_requirement_id": task.get("sub_requirement_id"),
        "sub_requirement_description": task.get("sub_requirement_description"),
        "rotation_id": task.get("rotation_id"),
        "rotation_index": task.get("rotation_index"),
        "rotation_size": task.get("rotation_size"),
        "reference_ordering_seed": task.get("reference_ordering_seed") or task.get("cs_ordering_seed"),
        "cs_ordering_seed": task.get("cs_ordering_seed"),
        "cs_option_keys": task.get("cs_option_keys"),
        "cs_option_labels": task.get("cs_option_labels"),
        "cs_option_services": task.get("cs_option_services"),
        "cs_render_style": task.get("cs_render_style"),
        "reference_option_keys": task.get("reference_option_keys") or task.get("cs_option_keys"),
        "reference_option_labels": task.get("reference_option_labels") or task.get("cs_option_labels"),
        "reference_option_services": task.get("reference_option_services") or task.get("cs_option_services"),
        "reference_render_style": task.get("cs_render_style"),
        "uniform_baseline": task.get("uniform_baseline"),
        "prompt_text": task.get("prompt_text"),
        "prompt_sha256": _sha256_text(task.get("prompt_text")),
        "system_prompt": system_prompt,
        "system_prompt_sha256": _sha256_text(system_prompt),
        "system_prompt_path": str(system_prompt_path_value) if system_prompt_path_value else None,
        "messages": messages,
        "messages_sha256": _sha256_json(messages),
        "completion_index": ci,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sampling": sampling_record,
        **result,
    }
    with open(filepath, "w") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)


def call_model(model_config, system_prompt, user_message, sampling):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    # Only pass sampling params that are explicitly set (not None)
    # None means "use provider default"
    kwargs = {"model": model_config["litellm_string"], "messages": messages}

    # Some models (e.g., reasoning models) only accept temperature=1
    # Skip temperature/top_p for these models to avoid API errors
    fixed_temp_models = model_config.get("fixed_temperature_only", False)

    if sampling.get("temperature") is not None and not fixed_temp_models:
        kwargs["temperature"] = sampling["temperature"]
    if sampling.get("max_tokens") is not None:
        kwargs["max_tokens"] = sampling["max_tokens"]
    if sampling.get("top_p") is not None and not fixed_temp_models:
        # Anthropic doesn't allow both temperature and top_p together
        if "anthropic" in model_config["litellm_string"] and "temperature" in kwargs:
            pass  # skip top_p when temperature is already set
        else:
            kwargs["top_p"] = sampling["top_p"]
    reasoning_effort, _reasoning_source = _reasoning_effort_sent_to_api(model_config, sampling)
    if reasoning_effort is not None:
        kwargs["reasoning_effort"] = reasoning_effort

    # Use custom base URL and/or API key if set (e.g., DashScope, Nova API, local vLLM)
    api_base_env = model_config.get("api_base_env")
    if api_base_env:
        api_base = os.environ.get(api_base_env)
        if api_base:
            kwargs["api_base"] = api_base
    else:
        dashscope_base = os.environ.get("DASHSCOPE_BASE_URL")
        if dashscope_base and "dashscope" in model_config["litellm_string"]:
            kwargs["api_base"] = dashscope_base

    # Pass API key explicitly for OpenAI-compatible endpoints (Nova, local vLLM, etc.)
    api_key_env = model_config.get("api_key_env")
    if api_key_env and api_base_env:
        api_key = os.environ.get(api_key_env)
        if api_key:
            kwargs["api_key"] = api_key

    start = time.time()
    try:
        response = litellm.completion(**kwargs)
        elapsed = time.time() - start
        usage = response.usage
        usage_dict = None
        if usage:
            if hasattr(usage, "model_dump"):
                usage_dict = usage.model_dump()
            elif isinstance(usage, dict):
                usage_dict = dict(usage)
        completion_details = (usage_dict or {}).get("completion_tokens_details") or {}
        prompt_details = (usage_dict or {}).get("prompt_tokens_details") or {}
        return {
            "output_text": response.choices[0].message.content,
            "finish_reason": response.choices[0].finish_reason,
            "input_tokens": getattr(usage, "prompt_tokens", None) if usage else None,
            "output_tokens": getattr(usage, "completion_tokens", None) if usage else None,
            "usage": usage_dict,
            "completion_tokens_details": completion_details,
            "prompt_tokens_details": prompt_details,
            "reasoning_tokens": completion_details.get("reasoning_tokens"),
            "elapsed_seconds": round(elapsed, 2),
            "error": None,
        }
    except Exception as e:
        return {
            "output_text": None,
            "finish_reason": "error",
            "input_tokens": None,
            "output_tokens": None,
            "elapsed_seconds": round(time.time() - start, 2),
            "error": {"type": type(e).__name__, "message": str(e)[:500]},
        }


# ---------------------------------------------------------------------------
# Run directory management
# ---------------------------------------------------------------------------

def create_run_dir(config, run_name=None):
    """Create a run directory with config and README.

    Nested config names are treated as stable canonical paths. Ad-hoc flat
    names keep the timestamped behavior to avoid overwriting exploratory runs.
    """
    if run_name and ("/" in run_name or "\\" in run_name):
        name = run_name
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"{timestamp}_{run_name}" if run_name else timestamp
    run_dir = RUNS_DIR / name
    run_dir.mkdir(parents=True, exist_ok=True)

    # Save effective config
    config_to_save = {k: v for k, v in config.items() if not k.startswith("_")}
    config_to_save["_meta"] = config.get("_source", {})
    with open(run_dir / "config.yaml", "w") as f:
        yaml.dump(config_to_save, f, default_flow_style=False, sort_keys=False)

    return run_dir, name


def write_run_readme(run_dir, run_name, config, models, tasks, total_calls, stats):
    """Write auto-generated README for this run."""
    now = datetime.now(timezone.utc)
    sampling = config["sampling"]
    sampling_mode = (
        "controlled"
        if _sampling_has_explicit_controls(sampling)
        else "provider_default"
    )

    lines = [
        f"# VIBench Run: {run_name}",
        f"",
        f"**Date**: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"**Status**: {'completed' if stats else 'started'}",
        f"",
        f"## Configuration",
        f"",
        f"- **Models**: {len(models)} — {', '.join(m['id'] for m in models)}",
        f"- **Modalities**: {', '.join(config['modalities'])}",
        f"- **Scenarios**: {config['scenarios']}",
        f"- **Completions per prompt**: {config['completions']}",
        f"- **Temperature**: {_format_sampling_banner(sampling['temperature'])}",
        f"- **Max tokens**: {_format_sampling_banner(sampling['max_tokens'])}",
        f"- **Top-p**: {_format_sampling_banner(sampling['top_p'])}",
        f"- **Reasoning effort**: {_format_sampling_banner(sampling.get('reasoning_effort'))}",
        f"- **Reasoning effort by model**: {_format_mapping_banner(sampling.get('reasoning_effort_by_model') or {})}",
        f"- **Reasoning effort policy**: {sampling.get('reasoning_effort_policy', 'supported_only')}",
        f"- **Sampling mode**: {sampling_mode}",
        f"- **Option order mode**: {config.get('option_order_mode', 'balanced')}",
        f"- **Total tasks**: {len(tasks)}",
        f"- **Total API calls**: {total_calls}",
        f"",
    ]

    # Source tracking
    source = config.get("_source", {})
    lines.append("## Config Sources")
    lines.append("")
    if "run_config" in source:
        lines.append(f"- **Run config**: `{source['run_config']}`")
    if "cli_overrides" in source:
        lines.append(f"- **CLI overrides**: `{source['cli_overrides']}`")
    lines.append(f"- **Default config**: `{source.get('default', 'N/A')}`")
    lines.append("")

    if stats:
        lines.extend([
            f"## Results",
            f"",
            f"- **Completed**: {stats['completed']}",
            f"- **Skipped** (already existed): {stats['skipped']}",
            f"- **Errors**: {stats['errors']}",
        ])
        if stats.get("aborted"):
            lines.append(f"- **Aborted** (skipped after fail-fast threshold): {stats['aborted']}")
        if stats.get("aborted_models"):
            lines.append(f"- **Models hit by fail-fast**: {', '.join(sorted(stats['aborted_models']))}")
        lines.extend([
            f"- **Duration**: {stats['duration']:.1f}s",
            f"",
        ])

    lines.extend([
        f"## Output Structure",
        f"",
        f"```",
        f"{run_dir.name}/",
        f"├── README.md       ← this file",
        f"├── config.yaml     ← effective configuration",
        f"└── raw/            ← API responses",
        f"    └── {{modality}}/",
        f"        └── {{model_id}}/",
        f"            └── {{task_id}}__c{{N}}.json",
        f"```",
    ])

    (run_dir / "README.md").write_text("\n".join(lines))


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------

def run(config, dry_run=False, run_name=None, verbose=False, force_sequential=False):
    env_path = resolve_path(config, "env_file")
    load_dotenv(env_path, override=True)

    system_prompt_path_value = system_prompt_path(config)
    system_prompt = load_system_prompt(config)
    models = load_models(config)
    validate_model_env(models, env_path)
    n_completions = config["completions"]
    sampling = config["sampling"]
    option_order_mode = config.get("option_order_mode", "balanced")
    sampling_mode = (
        "controlled"
        if _sampling_has_explicit_controls(sampling)
        else "provider_default"
    )

    # Per-call delay between API calls. The default `rate_limit_delay` is a
    # single value that applies to every model. Set `rate_limit_delay_per_model`
    # to a {model_id: seconds} dict to override on a per-model basis (e.g.
    # nova-pro at 18s, nova-2-lite at 4s in the same parallel run).
    default_delay = float(config.get("rate_limit_delay", 0.5) or 0.0)
    per_model_delay = dict(config.get("rate_limit_delay_per_model") or {})

    def _delay_for(model_id):
        return float(per_model_delay.get(model_id, default_delay))

    benchmark = config.get("benchmark", "vibench")

    # Build task list
    tasks = []
    for modality in config["modalities"]:
        assembler = ASSEMBLERS[modality]
        for scenario in load_scenario_files(config, modality):
            scenario["_benchmark"] = benchmark
            for task in assembler(scenario):
                task["benchmark"] = benchmark
                tasks.append(task)

    total_calls = len(tasks) * len(models) * n_completions

    # Print summary
    print("=" * 60)
    print(f"VIBench — Benchmark {benchmark.upper()}")
    print("=" * 60)
    print(f"  Benchmark:     {benchmark}")
    dataset_format = "hf_jsonl" if _uses_hf_direct_dataset(config) else "legacy_folders"
    print(f"  Datasets:      benchmark/{benchmark}/ ({dataset_format})")
    print(f"  Models:        {len(models)} — {[m['id'] for m in models]}")
    print(f"  Modalities:    {config['modalities']}")
    if _uses_hf_direct_dataset(config):
        scope = _provider_scope(config)
        if scope is not None:
            print(f"  Provider scope:{scope}")
        print(f"  Dataset file:  {_hf_direct_dataset_path(config)}")
    print(f"  Tasks:         {len(tasks)}")
    print(f"  Completions:   {n_completions} per task per model")
    print(
        "  Sampling:      "
        f"temp={_format_sampling_banner(sampling['temperature'])}, "
        f"max_tokens={_format_sampling_banner(sampling['max_tokens'])}, "
        f"top_p={_format_sampling_banner(sampling['top_p'])}, "
        f"reasoning_effort={_format_sampling_banner(sampling.get('reasoning_effort'))}, "
        f"reasoning_by_model={_format_mapping_banner(sampling.get('reasoning_effort_by_model') or {})}, "
        f"reasoning_policy={sampling.get('reasoning_effort_policy', 'supported_only')} "
        f"[mode={sampling_mode}]"
    )
    print(f"  Option order:  {option_order_mode}")
    print(f"  System:        {system_prompt_path_value}")
    print(f"  Total calls:   {total_calls}")
    if per_model_delay:
        # Show the per-model overrides explicitly so the user can verify
        # they're being applied to the right models.
        rate_summary = ", ".join(
            f"{m['id']}={_delay_for(m['id'])}s" for m in models
        )
        print(f"  Rate limit:    {rate_summary}")
    else:
        print(f"  Rate limit:    {default_delay}s between calls")
    print(f"  Mode:          {'verbose' if verbose else 'progress bar'}")
    print(f"  Env file:      {env_path}")
    print(f"  Credentials:")
    for model in models:
        required = ", ".join(required_env_vars_for_model(model))
        print(f"    - {model['id']}: {required}")
    print()

    if dry_run:
        print("DRY RUN — task list:\n")
        for task in tasks:
            preview = task["prompt_text"][:80].replace("\n", " ")
            print(f"  [{task['modality']:15s}] {task['task_id']:15s} | {preview}...")
        print(f"\nWould execute {total_calls} API calls across {len(models)} models.")
        return

    # Create or resume run directory
    resume_dir = config.get("_resume_dir")
    if resume_dir:
        run_dir = Path(resume_dir)
        try:
            effective_name = run_dir.relative_to(RUNS_DIR).as_posix()
        except ValueError:
            effective_name = run_dir.name
        print(f"  RESUMING into: {run_dir}")
    else:
        run_dir, effective_name = create_run_dir(config, run_name)
        print(f"  Run directory: {run_dir}")
    print()

    # Write initial README
    write_run_readme(run_dir, effective_name, config, models, tasks, total_calls, stats=None)

    # Build jobs grouped by model (for parallel execution)
    # Each model's jobs run sequentially (respects per-provider rate limits)
    # Different models run in parallel (different API providers)
    model_jobs = {}
    total_jobs = 0
    job_limit = config.get("limit_per_model")
    for model in models:
        model_jobs[model["id"]] = []
        for task in tasks:
            for ci in range(1, n_completions + 1):
                model_jobs[model["id"]].append((task, model, ci))
        if job_limit:
            model_jobs[model["id"]] = model_jobs[model["id"]][:job_limit]
        total_jobs += len(model_jobs[model["id"]])

    # Shared counters (thread-safe via lock)
    import threading
    lock = threading.Lock()
    stats = {"completed": 0, "skipped": 0, "errors": 0, "aborted": 0}
    start_time = time.time()

    # Per-model fail-fast: stop scheduling new tasks for a model after N
    # consecutive errors. Disabled by default. Useful when a provider is
    # rate-limited or otherwise broken — instead of burning through 1000
    # more failed calls we bail out early on that model and let the others
    # keep running. The skip-existing check still runs first so we never
    # double-spend on completed work.
    max_consecutive_errors = int(config.get("max_consecutive_errors") or 0)
    consecutive_errors = {}      # model_id -> int
    aborted_models = set()       # model_ids that hit the threshold

    def _record_result(model_id, has_error):
        """Update the consecutive-error counter and possibly mark a model
        as aborted. Caller must hold `lock`."""
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

    # Resume skip-existence check. By default we look at labeled/ rather
    # than raw/ so a run that ships only labeled files is still
    # resume-safe. Set skip_from to "raw" to use the legacy behaviour, or
    # "both" to skip a slot if either tree has the file.
    skip_from = (config.get("skip_from") or "labeled").lower()
    if skip_from not in ("labeled", "raw", "both"):
        print(f"  WARN: unknown skip_from={skip_from!r}, falling back to 'labeled'")
        skip_from = "labeled"
    retry_errors = bool(config.get("retry_errors"))
    retry_empty = bool(config.get("retry_empty"))

    def _record_needs_retry(path):
        """Return True when an existing output should be regenerated."""
        if not (retry_errors or retry_empty):
            return False
        try:
            with open(path) as fh:
                record = json.load(fh)
        except (OSError, json.JSONDecodeError):
            return True

        if retry_errors and record.get("error"):
            return True
        if retry_empty and not (record.get("output_text") or "").strip():
            return True
        return False

    def _already_done(task, model_id, ci):
        fname = f"{task['task_id']}__c{ci}.json"
        rel = Path(task["modality"]) / model_id / fname
        existing = []
        if skip_from in ("labeled", "both"):
            path = run_dir / "labeled" / rel
            if path.exists():
                existing.append(path)
        if skip_from in ("raw", "both"):
            path = run_dir / "raw" / rel
            if path.exists():
                existing.append(path)
        if not existing:
            return False
        return any(not _record_needs_retry(path) for path in existing)

    def _process_model_jobs(model_id, jobs_for_model, pbar=None):
        """Process all jobs for one model sequentially."""
        for task, model, ci in jobs_for_model:
            output_dir = run_dir / "raw" / task["modality"] / model["id"]
            output_dir.mkdir(parents=True, exist_ok=True)
            filepath = output_dir / f"{task['task_id']}__c{ci}.json"

            if _already_done(task, model["id"], ci):
                with lock:
                    stats["skipped"] += 1
                if pbar:
                    pbar.update(1)
                continue

            # Per-model fail-fast: if this model has been aborted, advance
            # the progress bar without making the API call.
            if model_id in aborted_models:
                with lock:
                    stats["aborted"] += 1
                if pbar:
                    pbar.update(1)
                continue

            call_task = (
                _materialize_cs_task(
                    task,
                    ci,
                    option_order_mode=option_order_mode,
                    affiliation=model.get("ecosystem_affiliation"),
                )
                if _is_reference_modality(task["modality"])
                else task
            )
            result = call_model(model, system_prompt, call_task["prompt_text"], sampling)

            with lock:
                stats["completed"] += 1
                if result["error"]:
                    stats["errors"] += 1
                _record_result(model_id, has_error=bool(result["error"]))

            _save_record(
                filepath,
                call_task,
                model,
                ci,
                sampling,
                result,
                system_prompt=system_prompt,
                system_prompt_path_value=system_prompt_path_value,
            )

            if pbar:
                mod_short = (
                    "REF" if _is_reference_modality(task["modality"])
                    else task["modality"].upper()
                )
                pbar.set_postfix_str(
                    f"{mod_short}|{model_id[:20]}|{task['task_id']}|err={stats['errors']}"
                )
                pbar.update(1)

            if verbose:
                tag = f"[{stats['completed'] + stats['skipped']}/{total_jobs}]"
                if result["error"]:
                    print(f"{tag} {task['task_id']} × {model['id']} × c{ci} ... "
                          f"ERROR: {result['error']['type']}: {result['error']['message'][:60]}")
                else:
                    snippet = (result["output_text"] or "")[:60].replace("\n", " ")
                    print(f"{tag} {task['task_id']} × {model['id']} × c{ci} ... "
                          f"OK ({result['elapsed_seconds']}s) | {snippet}...")

            time.sleep(_delay_for(model_id))

    max_workers = config.get("max_workers") or len(models)
    parallel = len(models) > 1 and not verbose and not force_sequential
    n_workers = min(max_workers, len(models)) if parallel else 1

    if parallel:
        print(f"  Parallel: {n_workers} workers for {len(models)} models\n")

        # One progress bar per model + one total bar
        # Position 0 = total, positions 1..N = per model
        pbar_total = tqdm(
            total=total_jobs, desc="Total", position=0, unit="call",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
        )
        model_pbars = {}
        for idx, model_id in enumerate(model_jobs.keys(), start=1):
            n_model_jobs = len(model_jobs[model_id])
            model_pbars[model_id] = tqdm(
                total=n_model_jobs, desc=f"  {model_id[:28]:28s}", position=idx, unit="call",
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}]",
                leave=False,
            )

        def _parallel_process(model_id, jobs_for_model):
            model_pbar = model_pbars[model_id]
            for task, model, ci in jobs_for_model:
                output_dir = run_dir / "raw" / task["modality"] / model["id"]
                output_dir.mkdir(parents=True, exist_ok=True)
                filepath = output_dir / f"{task['task_id']}__c{ci}.json"

                if _already_done(task, model["id"], ci):
                    with lock:
                        stats["skipped"] += 1
                    model_pbar.update(1)
                    pbar_total.update(1)
                    continue

                # Per-model fail-fast: drain the queue without spending tokens
                if model_id in aborted_models:
                    with lock:
                        stats["aborted"] += 1
                    model_pbar.update(1)
                    pbar_total.update(1)
                    continue

                call_task = (
                    _materialize_cs_task(
                        task,
                        ci,
                        option_order_mode=option_order_mode,
                        affiliation=model.get("ecosystem_affiliation"),
                    )
                    if _is_reference_modality(task["modality"])
                    else task
                )
                result = call_model(model, system_prompt, call_task["prompt_text"], sampling)

                with lock:
                    stats["completed"] += 1
                    if result["error"]:
                        stats["errors"] += 1
                    _record_result(model_id, has_error=bool(result["error"]))

                _save_record(
                    filepath,
                    call_task,
                    model,
                    ci,
                    sampling,
                    result,
                    system_prompt=system_prompt,
                    system_prompt_path_value=system_prompt_path_value,
                )
                model_pbar.update(1)
                pbar_total.update(1)
                time.sleep(_delay_for(model_id))

        with ThreadPoolExecutor(max_workers=n_workers) as executor:
            futures = {}
            for model_id, jobs_for_model in model_jobs.items():
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
        # Sequential: verbose or single model or forced
        if verbose:
            # Verbose mode: per-call text output
            for model_id, jobs_for_model in model_jobs.items():
                _process_model_jobs(model_id, jobs_for_model, pbar=None)
        else:
            pbar = tqdm(total=total_jobs, desc="Total", unit="call")
            for model_id, jobs_for_model in model_jobs.items():
                _process_model_jobs(model_id, jobs_for_model, pbar)
            pbar.close()

    duration = time.time() - start_time
    stats["duration"] = duration

    # Update README with final stats
    write_run_readme(run_dir, effective_name, config, models, tasks, total_calls, stats)

    print()
    print("=" * 60)
    summary = (
        f"Done. Completed: {stats['completed']}, "
        f"Skipped: {stats['skipped']}, "
        f"Errors: {stats['errors']}"
    )
    if stats.get("aborted"):
        summary += f", Aborted: {stats['aborted']}"
    if aborted_models:
        summary += f"  (fail-fast hit: {', '.join(sorted(aborted_models))})"
        # Carry the aborted-models set into the run README writer.
        stats["aborted_models"] = sorted(aborted_models)
    print(summary)
    print(f"Duration: {duration:.1f}s")
    if len(models) > 1:
        print(f"Mode: {'parallel' if parallel else 'sequential'} ({len(models)} models)")
    print(f"Run directory: {run_dir}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="VIBench Direct Mode Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/generation/run_direct.py --config configs/vibench/direct/complete/full_5c.yaml --resume direct/complete/full_5c
  python scripts/generation/run_direct.py --config configs/vibench/direct/complete/full_5c.yaml --dry-run
  python scripts/generation/run_direct.py --config configs/vibench/direct/complete/full_5c.yaml --model gemini-2.5-flash --scenario S05 --completions 1
  python scripts/generation/run_direct.py --config configs/vibench/direct/complete/full_5c.yaml --scenario S19 S20
        """,
    )
    parser.add_argument("--config", type=str, default=None,
                        help="Path to YAML run config")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would run without calling APIs")
    parser.add_argument("--name", type=str, default=None,
                        help="Custom run name. Names containing '/' are used as stable paths under outputs/runs/.")
    parser.add_argument("--resume", type=str, default=None,
                        help="Resume into an existing run directory (by name or path)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show per-call output instead of progress bar (forces sequential)")
    parser.add_argument("--sequential", action="store_true",
                        help="Force sequential execution even with multiple models")
    parser.add_argument("--workers", type=int, default=None,
                        help="Max parallel workers (default: one per model)")

    override = parser.add_argument_group("overrides (take precedence over YAML config)")
    override.add_argument("--benchmark",
                          help="Benchmark family. Only the current vibench benchmark is kept locally.")
    override.add_argument("--model", type=str, nargs="+",
                          help="Run only these model ID(s) — pass multiple after the flag, "
                               "e.g. --model nova-pro nova-2-lite. Supersedes the YAML config.")
    override.add_argument("--scenario", type=str, nargs="+",
                          help="Run only these scenario IDs. Supports space-separated or comma-separated values, "
                               "for example --scenario S19 S20 or --scenario S19,S20")
    override.add_argument("--modality", choices=["nli", "fim", OPEN_REFERENCE_MODALITY, LEGACY_CS_MODALITY])
    override.add_argument("--limit", type=int,
                          help="Max generations per model (truncates the job queue; for smoke tests)")
    override.add_argument("--completions", type=int, help="Completions per prompt")
    override.add_argument("--temperature", type=float, help="Sampling temperature")
    override.add_argument("--max-tokens", type=int, help="Max output tokens")
    override.add_argument("--reasoning-effort",
                          choices=["none", "low", "medium", "high", "xhigh"],
                          help="Optional reasoning effort for routes that support it")
    override.add_argument("--rate-limit-delay", type=float, nargs="+",
                          help="Seconds to wait between calls per worker. Pass one value to apply "
                               "to every model, or multiple values matched positionally with the "
                               "--model list (e.g. --model nova-pro nova-2-lite "
                               "--rate-limit-delay 18 4 → nova-pro at 18s, nova-2-lite at 4s).")
    override.add_argument("--skip-from", choices=["labeled", "raw", "both"],
                          default=None,
                          help="On resume, decide whether a task is already done by checking labeled/, "
                               "raw/, or both. Default is 'labeled' (canonical curated runs ship only "
                               "labeled/), set to 'raw' to use the legacy behaviour or 'both' to skip "
                               "if either tree has the file.")
    override.add_argument("--retry-errors", action="store_true",
                          help="On resume, regenerate existing outputs whose JSON record has a non-empty "
                               "error field instead of treating them as already done.")
    override.add_argument("--retry-empty", action="store_true",
                          help="On resume, regenerate existing outputs whose output_text is empty instead "
                               "of treating them as already done.")
    override.add_argument("--max-consecutive-errors", type=int, default=None,
                          help="Stop scheduling new tasks for a model after N consecutive errors. "
                               "0 disables (default). Useful when a provider is rate-limited or "
                               "broken — fails the model fast instead of burning through hundreds "
                               "of failed calls. Per-model: other models keep running.")

    args = parser.parse_args()

    config = load_config(args.config)
    config = apply_cli_overrides(config, args)

    # Name priority: CLI --name > YAML name > none
    if args.workers is not None:
        config["max_workers"] = args.workers

    # Resume: resolve run directory path. Searches an absolute path first,
    # then outputs/runs/, allowing both exact-name and substring matches.
    if args.resume:
        resume_path = resolve_existing_run(args.resume)
        if resume_path is None:
            print(f"Cannot find run to resume: {args.resume}  "
                  f"(searched outputs/runs/)")
            return
        config["_resume_dir"] = str(resume_path)
        print(f"Resuming run: {resume_path}")

    run_name = args.name or config.get("name")
    run(config, dry_run=args.dry_run, run_name=run_name, verbose=args.verbose,
        force_sequential=args.sequential)


if __name__ == "__main__":
    main()
