"""
VIBench agentic runner using OpenAI Agents SDK + LiteLLM.

This runner is intentionally separate from run_agentic.py, which uses
OpenCode. It keeps the same benchmark task loading and prompt construction,
but exposes a single write_file tool to the model and routes model calls
through LiteLLM.
"""

import argparse
import asyncio
import json
import os
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import threading

import yaml
from dotenv import load_dotenv
from tqdm import tqdm

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from agents import Agent, ModelSettings, RunConfig, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel

from run_agentic import (
    BASE_DIR,
    RUNS_DIR,
    _resolve_existing_run,
    _agentic_job_label,
    _agentic_output_id,
    _benchmark_paths,
    _canonical_benchmark_name,
    _component_is_scored,
    _expand_tasks_for_seed_conditions,
    _format_mapping_banner,
    _format_sampling_banner,
    _load_agentic_system_prompt,
    _load_direct_reference_cards,
    _materialize_seed_files,
    _normalize_seed_condition_request,
    _resolve_agentic_system_prompt_path,
    _sha256_json,
    _sha256_text,
    build_agentic_prompt,
    collect_files,
    load_models,
    load_tasks,
    required_env_vars_for_model,
    resolve_primary_component,
    validate_model_env,
)
from run_direct import (
    _reasoning_effort_request,
    _reasoning_effort_sent_to_api,
)


DEFAULT_CONFIG = {
    "type": "agentic_litellm_agents",
    "benchmark": "vibench",
    "completions": 1,
    "variants": ["free", "informed"],
    "models": "all",
    "tasks": "all",
    "timeout": 300,
    "max_turns": 30,
    "max_workers": None,
    "rate_limit_delay": 0.0,
    "rate_limit_delay_per_model": {},
    "max_consecutive_errors": 5,
    "sampling": {},
}


AGENT_TOOL_INSTRUCTION = """
Tool execution requirements:
- Create files by calling write_file(path, content). Do not print code as the final answer instead of writing files.
- Call write_file for every requested file, using exactly the requested relative filename.
- The final answer should be a short completion marker after the files are written.
""".strip()


def _load_config(config_path=None):
    config = dict(DEFAULT_CONFIG)
    if config_path and Path(config_path).exists():
        with open(config_path) as f:
            run_config = yaml.safe_load(f) or {}
        config.update(run_config)
        config["_source"] = {"run_config": str(Path(config_path).resolve())}
    else:
        config["_source"] = {}
    return config


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


def _apply_cli_overrides(config, args):
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
    if args.max_turns is not None:
        config["max_turns"] = args.max_turns
        overrides["max_turns"] = args.max_turns
    if args.max_consecutive_errors is not None:
        config["max_consecutive_errors"] = args.max_consecutive_errors
        overrides["max_consecutive_errors"] = args.max_consecutive_errors
    if args.workers is not None:
        config["max_workers"] = args.workers
        overrides["max_workers"] = args.workers
    if args.seed_condition:
        config["seed_conditions"] = _normalize_seed_condition_request(args.seed_condition)
        overrides["seed_condition"] = args.seed_condition
    if args.retry_errors:
        config["retry_errors"] = True
        overrides["retry_errors"] = True
    if args.retry_empty:
        config["retry_empty"] = True
        overrides["retry_empty"] = True
    if args.retry_incomplete:
        config["retry_incomplete"] = True
        overrides["retry_incomplete"] = True
    if overrides:
        config["_source"]["cli_overrides"] = overrides
    return config


def _sampling_has_explicit_controls(sampling):
    return any(
        sampling.get(k) is not None
        for k in ("temperature", "max_tokens", "top_p", "reasoning_effort")
    ) or bool(sampling.get("reasoning_effort_by_model"))


def _build_sampling_record(model_config, sampling):
    sampling = sampling or {}
    fixed_temp_models = model_config.get("fixed_temperature_only", False)
    temperature_sent = None
    top_p_sent = None
    max_tokens_sent = sampling.get("max_tokens") if sampling.get("max_tokens") is not None else None
    top_p_source = "explicit" if sampling.get("top_p") is not None else "provider_default"

    if sampling.get("temperature") is not None and not fixed_temp_models:
        temperature_sent = sampling["temperature"]
    if sampling.get("top_p") is not None and not fixed_temp_models:
        if "anthropic" in model_config.get("litellm_string", "") and temperature_sent is not None:
            top_p_source = "skipped_for_anthropic_temperature"
        else:
            top_p_sent = sampling["top_p"]

    reasoning_requested, reasoning_source = _reasoning_effort_request(model_config, sampling)
    reasoning_sent, reasoning_sent_source = _reasoning_effort_sent_to_api(model_config, sampling)

    return {
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
        "parallel_tool_calls": sampling.get("parallel_tool_calls"),
        "tool_choice": sampling.get("tool_choice"),
    }


def _build_model_settings(model_config, sampling):
    record = _build_sampling_record(model_config, sampling)
    extra_args = {}
    if record["reasoning_effort_sent_to_api"] is not None:
        extra_args["reasoning_effort"] = record["reasoning_effort_sent_to_api"]

    return ModelSettings(
        temperature=record["temperature_sent_to_api"],
        top_p=record["top_p_sent_to_api"],
        max_tokens=record["max_tokens_sent_to_api"],
        parallel_tool_calls=record["parallel_tool_calls"],
        tool_choice=record["tool_choice"],
        extra_args=extra_args or None,
    )


def _resolve_litellm_base_url(model_config):
    api_base_env = model_config.get("api_base_env")
    if api_base_env:
        return os.environ.get(api_base_env)
    if "dashscope" in model_config.get("litellm_string", ""):
        return os.environ.get("DASHSCOPE_BASE_URL") or None
    return None


def _resolve_litellm_api_key(model_config):
    api_key_env = model_config.get("api_key_env")
    if not api_key_env:
        return None
    if model_config.get("api_base_env"):
        return os.environ.get(api_key_env)
    return None


def _json_safe(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if hasattr(value, "model_dump"):
        return _json_safe(value.model_dump())
    if hasattr(value, "__dict__"):
        return _json_safe({
            k: v for k, v in value.__dict__.items()
            if not k.startswith("_")
        })
    return repr(value)


def _summarize_run_result(result):
    raw_responses = []
    for response in getattr(result, "raw_responses", []) or []:
        usage = getattr(response, "usage", None)
        raw_responses.append({
            "response_id": getattr(response, "response_id", None),
            "output_count": len(getattr(response, "output", []) or []),
            "usage": _json_safe(usage),
        })
    return {
        "final_output": _json_safe(getattr(result, "final_output", None)),
        "raw_response_count": len(raw_responses),
        "raw_responses": raw_responses,
        "new_item_count": len(getattr(result, "new_items", []) or []),
        "max_turns": getattr(result, "max_turns", None),
    }


def _normalize_tool_path(path):
    normalized = PurePosixPath(str(path).replace("\\", "/")).as_posix()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def _make_agent_instructions(system_prompt):
    parts = []
    if system_prompt:
        parts.append(system_prompt.strip())
    parts.append(AGENT_TOOL_INSTRUCTION)
    return "\n\n".join(parts).strip()


def _make_agent_user_prompt(prompt, expected_files):
    expected = "\n".join(f"- {fname}" for fname in expected_files)
    return "\n\n".join([
        prompt.strip(),
        "Expected files that must be written with write_file:",
        expected,
        "Use write_file for each expected file before producing the final answer.",
    ]).strip()


def _make_write_file_tool(workspace_dir, expected_files, tool_calls):
    expected = set(expected_files)

    @function_tool
    def write_file(path: str, content: str) -> str:
        """Write one requested Python source file into the benchmark workspace."""
        normalized = _normalize_tool_path(path)
        call = {
            "path": path,
            "normalized_path": normalized,
            "content_sha256": _sha256_text(content),
            "content_length": len(content or ""),
            "accepted": False,
            "message": None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if normalized not in expected:
            call["message"] = (
                f"Rejected path {normalized!r}. Use exactly one of: "
                f"{', '.join(sorted(expected))}."
            )
            tool_calls.append(call)
            return "ERROR: " + call["message"]

        target = workspace_dir / normalized
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content or "")
        call["accepted"] = True
        call["message"] = f"Wrote {normalized}."
        tool_calls.append(call)
        return call["message"]

    return write_file


async def run_agents_sdk(
    task,
    prompt,
    workspace_dir,
    model_config,
    timeout,
    max_turns,
    system_prompt="",
    system_prompt_path=None,
    sampling=None,
    verbose=False,
):
    sampling = sampling or {}
    tool_calls = []
    seed_files = _materialize_seed_files(workspace_dir, task or {})
    agent_instructions = _make_agent_instructions(system_prompt)
    user_prompt = _make_agent_user_prompt(prompt, task["expected_files"])
    sampling_record = _build_sampling_record(model_config, sampling)
    model_settings = _build_model_settings(model_config, sampling)
    litellm_model = LitellmModel(
        model=model_config["litellm_string"],
        base_url=_resolve_litellm_base_url(model_config),
        api_key=_resolve_litellm_api_key(model_config),
    )
    write_file = _make_write_file_tool(workspace_dir, task["expected_files"], tool_calls)
    agent = Agent(
        name="vibench_file_writer",
        instructions=agent_instructions,
        model=litellm_model,
        model_settings=model_settings,
        tools=[write_file],
    )
    run_config = RunConfig(
        tracing_disabled=True,
        workflow_name="vibench_litellm_agents",
    )

    if verbose:
        print(f"    Workspace: {workspace_dir}")
        print(f"    LiteLLM model: {model_config['litellm_string']}")
        print(f"    Max turns: {max_turns}")
        print(f"    Prompt length: {len(user_prompt)} chars")

    start = time.time()
    try:
        result = await asyncio.wait_for(
            Runner.run(
                agent,
                user_prompt,
                max_turns=max_turns,
                run_config=run_config,
            ),
            timeout=timeout,
        )
        elapsed = time.time() - start
        summary = _summarize_run_result(result)
        return {
            "exit_code": 0,
            "elapsed_seconds": round(elapsed, 2),
            "error": None,
            "stdout": str(summary.get("final_output") or ""),
            "stderr": "",
            "agentic_runner": "litellm_openai_agents",
            "agentic_system_prompt_mode": "openai_agents_litellm_write_file_tool",
            "litellm_model": model_config["litellm_string"],
            "litellm_base_url": _resolve_litellm_base_url(model_config),
            "agent_name": "vibench_file_writer",
            "agent_instructions": agent_instructions,
            "agent_instructions_sha256": _sha256_text(agent_instructions),
            "agent_tool_instruction": AGENT_TOOL_INSTRUCTION,
            "prompt_text": prompt,
            "prompt_sha256": _sha256_text(prompt),
            "agent_user_prompt": user_prompt,
            "agent_user_prompt_sha256": _sha256_text(user_prompt),
            "system_prompt": system_prompt,
            "system_prompt_sha256": _sha256_text(system_prompt),
            "system_prompt_path": str(system_prompt_path) if system_prompt_path else None,
            "sampling": sampling_record,
            "model_settings": _json_safe(model_settings),
            "max_turns": max_turns,
            "seed_files": seed_files,
            "tool_calls": tool_calls,
            "tool_call_count": len(tool_calls),
            "accepted_tool_call_count": sum(1 for call in tool_calls if call.get("accepted")),
            "run_result": summary,
        }
    except Exception as exc:
        elapsed = time.time() - start
        return {
            "exit_code": -1,
            "elapsed_seconds": round(elapsed, 2),
            "error": {
                "type": type(exc).__name__,
                "message": str(exc)[:2000],
            },
            "stdout": "",
            "stderr": str(exc),
            "agentic_runner": "litellm_openai_agents",
            "agentic_system_prompt_mode": "openai_agents_litellm_write_file_tool",
            "litellm_model": model_config["litellm_string"],
            "litellm_base_url": _resolve_litellm_base_url(model_config),
            "agent_name": "vibench_file_writer",
            "agent_instructions": agent_instructions,
            "agent_instructions_sha256": _sha256_text(agent_instructions),
            "agent_tool_instruction": AGENT_TOOL_INSTRUCTION,
            "prompt_text": prompt,
            "prompt_sha256": _sha256_text(prompt),
            "agent_user_prompt": user_prompt,
            "agent_user_prompt_sha256": _sha256_text(user_prompt),
            "system_prompt": system_prompt,
            "system_prompt_sha256": _sha256_text(system_prompt),
            "system_prompt_path": str(system_prompt_path) if system_prompt_path else None,
            "sampling": sampling_record,
            "model_settings": _json_safe(model_settings),
            "max_turns": max_turns,
            "seed_files": seed_files,
            "tool_calls": tool_calls,
            "tool_call_count": len(tool_calls),
            "accepted_tool_call_count": sum(1 for call in tool_calls if call.get("accepted")),
            "run_result": None,
        }


def _save_agentic_output(out_dir, task, model, variant, ci, result, generated_files, workspace):
    out_dir.mkdir(parents=True, exist_ok=True)
    primary = resolve_primary_component(task)
    scored_files = set(task.get("scored_files", []))
    seed_files = result.get("seed_files") or []
    seeded_file_names = {
        seed.get("file")
        for seed in seed_files
        if isinstance(seed, dict) and seed.get("file")
    }
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
        "direct_provider_affiliation": model.get("direct_provider_affiliation"),
        "provider_family": model.get("provider_family"),
        "ecosystem_affiliation": model.get("ecosystem_affiliation") or model.get("cloud_affiliation"),
        "completion_index": ci,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prompt_text": result.get("prompt_text"),
        "prompt_sha256": result.get("prompt_sha256"),
        "system_prompt": result.get("system_prompt"),
        "system_prompt_sha256": result.get("system_prompt_sha256"),
        "system_prompt_path": result.get("system_prompt_path"),
        "agent_user_prompt": result.get("agent_user_prompt"),
        "agent_user_prompt_sha256": result.get("agent_user_prompt_sha256"),
        "agent_instructions": result.get("agent_instructions"),
        "agent_instructions_sha256": result.get("agent_instructions_sha256"),
        "agent_tool_instruction": result.get("agent_tool_instruction"),
        "sampling": result.get("sampling"),
        "model_settings": result.get("model_settings"),
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
        "agentic_runner": result.get("agentic_runner"),
        "agentic_system_prompt_mode": result.get("agentic_system_prompt_mode"),
        "agentic_identity_mode": "litellm_exact_or_provider_route",
        "agentic_identity_note": "OpenAI Agents SDK LitellmModel routes directly through LiteLLM; no OpenCode provider transform is used.",
        "litellm_model": result.get("litellm_model"),
        "litellm_base_url": result.get("litellm_base_url"),
        "agent_name": result.get("agent_name"),
        "agents_sdk_exit_code": result["exit_code"],
        "agents_sdk_stdout_tail": (result.get("stdout") or "")[-4000:],
        "agents_sdk_stderr_tail": (result.get("stderr") or "")[-4000:],
        "tool_calls": result.get("tool_calls") or [],
        "tool_call_count": result.get("tool_call_count"),
        "accepted_tool_call_count": result.get("accepted_tool_call_count"),
        "run_result": result.get("run_result"),
        "generation_warning": "NoFilesProduced" if (result.get("error") is None and not files_present) else None,
        "error": result["error"] or ({
            "type": "NoFilesProduced",
            "message": "Agents SDK run ended without an explicit process error, but none of the expected files were generated.",
        } if not files_present else None),
    }

    with open(out_dir / "_meta.json", "w") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    try:
        shutil.rmtree(workspace)
    except OSError as exc:
        print(f"  WARNING: workspace cleanup failed for {workspace}: {exc}")


def _run_needs_retry(out_dir, task, retry_errors=False, retry_empty=False, retry_incomplete=False):
    if not (retry_errors or retry_empty or retry_incomplete):
        return False
    meta_path = out_dir / "_meta.json"
    try:
        with open(meta_path) as f:
            meta = json.load(f)
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


def _resolve_run_dir(args, config):
    if args.resume:
        resolved = _resolve_existing_run(args.resume)
        if resolved is None:
            raise SystemExit(f"Cannot find run to resume: {args.resume}")
        try:
            run_name = resolved.relative_to(RUNS_DIR).as_posix()
        except ValueError:
            run_name = resolved.name
        return resolved, run_name

    name_suffix = args.name or config.get("name", "agentic_litellm_agents")
    if "/" in name_suffix or "\\" in name_suffix:
        run_name = name_suffix
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_name = f"{timestamp}_{name_suffix}"
    return RUNS_DIR / run_name, run_name


def _write_readme(run_dir, run_name, tasks, task_runs, active_seed_conditions, models, variants, n_completions, sampling, max_turns, scheduled, completed, skipped, errors, aborted, duration):
    sampling_mode = "controlled" if _sampling_has_explicit_controls(sampling) else "provider_default"
    readme = [
        f"# VIBench Agentic LiteLLM Agents Run: {run_name}",
        "",
        f"**Date**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"**Runner**: OpenAI Agents SDK + LiteLLM",
        f"**Tasks**: {len(tasks)} - {[t['task_id'] for t in tasks]}",
        f"**Seed conditions**: {active_seed_conditions if active_seed_conditions else []}",
        f"**Task cells**: {len(task_runs)}",
        f"**Models**: {len(models)} - {[m['id'] for m in models]}",
        f"**Variants**: {variants}",
        f"**Completions**: {n_completions}",
        f"**Max turns**: {max_turns}",
        f"**Sampling**: temp={_format_sampling_banner(sampling.get('temperature'))}, max_tokens={_format_sampling_banner(sampling.get('max_tokens'))}, top_p={_format_sampling_banner(sampling.get('top_p'))}, reasoning_effort={_format_sampling_banner(sampling.get('reasoning_effort'))}, reasoning_by_model={_format_mapping_banner(sampling.get('reasoning_effort_by_model') or {})}, reasoning_policy={sampling.get('reasoning_effort_policy', 'supported_only')} [mode={sampling_mode}]",
        f"**Scheduled**: {scheduled}",
        f"**Completed**: {completed}, Skipped: {skipped}, Errors: {errors}, Aborted: {aborted}",
        f"**Duration**: {duration:.1f}s",
        "",
        "## Output Structure",
        "",
        "```",
        "raw/agentic/{model_id}/{task_id}__{variant}__c{N}/",
        "├── component_a.py",
        "├── component_b.py",
        "├── ...",
        "└── _meta.json",
        "```",
    ]
    (run_dir / "README.md").write_text("\n".join(readme))


def main():
    parser = argparse.ArgumentParser(
        description="VIBench Agentic Benchmark Runner using OpenAI Agents SDK + LiteLLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--config", type=str, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--name", type=str, default=None,
                        help="Custom run name. Names containing '/' are used as stable paths under outputs/runs/.")
    parser.add_argument("--resume", type=str, default=None)
    parser.add_argument("--verbose", "-v", action="store_true")

    override = parser.add_argument_group("overrides")
    override.add_argument("--task", type=str, nargs="+",
                          help="Task suffixes or full task IDs. Supports space-separated or comma-separated values, "
                               "for example --task S19 S20 or --task S19,S20. Use all to run everything.")
    override.add_argument("--model", type=str, help="Model ID from models.json")
    override.add_argument("--variant", choices=["free", "informed", "both"])
    override.add_argument("--completions", type=int)
    override.add_argument("--timeout", type=int)
    override.add_argument("--max-turns", type=int)
    override.add_argument("--workers", type=int)
    override.add_argument("--sequential", action="store_true")
    override.add_argument("--max-consecutive-errors", type=int, default=None)
    override.add_argument("--seed-condition", type=str)
    override.add_argument("--retry-errors", action="store_true")
    override.add_argument("--retry-empty", action="store_true")
    override.add_argument("--retry-incomplete", action="store_true")
    args = parser.parse_args()

    config = _apply_cli_overrides(_load_config(args.config), args)
    benchmark = config.get("benchmark", "vibench")
    provider_scope = config.get("provider_scope")
    if provider_scope is None and _canonical_benchmark_name(benchmark) != "vibench":
        provider_scope = "all_available"

    reference_cards = _load_direct_reference_cards(benchmark, provider_scope=provider_scope)
    system_prompt_file = config.get("system_prompt_file")
    system_prompt_path = _resolve_agentic_system_prompt_path(benchmark, system_prompt_file)
    system_prompt = _load_agentic_system_prompt(benchmark, system_prompt_file)

    env_path = BASE_DIR / "configs" / ".env"
    load_dotenv(env_path, override=True)

    task_filter = config.get("tasks", "all")
    if task_filter == "all":
        tasks = load_tasks(benchmark=benchmark)
    else:
        tasks = []
        for task_id in (task_filter if isinstance(task_filter, list) else [task_filter]):
            tasks.extend(load_tasks(task_id, benchmark=benchmark))

    model_filter = config.get("models", "all")
    if model_filter == "all":
        models = load_models(benchmark=benchmark)
    else:
        models = []
        for model_id in (model_filter if isinstance(model_filter, list) else [model_filter]):
            models.extend(load_models(model_id, benchmark=benchmark))
    validate_model_env(models, env_path)

    for task in tasks:
        task["_benchmark"] = benchmark
    task_runs, active_seed_conditions = _expand_tasks_for_seed_conditions(
        tasks,
        config.get("seed_conditions"),
    )

    variants = config["variants"]
    n_completions = int(config["completions"])
    timeout = int(config.get("timeout", 300))
    max_turns = int(config.get("max_turns", 30))
    sampling = config.get("sampling", {}) or {}
    option_order_mode = config.get("option_order_mode", "balanced")
    max_consecutive_errors = int(config.get("max_consecutive_errors") or 0)
    tasks_path, models_path = _benchmark_paths(benchmark)
    if not models_path.exists():
        models_path = BASE_DIR / "benchmark" / "models.json"

    total = len(task_runs) * len(models) * len(variants) * n_completions
    sampling_mode = "controlled" if _sampling_has_explicit_controls(sampling) else "provider_default"

    print("=" * 60)
    print("VIBench Agentic Benchmark (LiteLLM + OpenAI Agents SDK)")
    print("=" * 60)
    print(f"  Benchmark:   {benchmark}")
    print(f"  Tasks file:  {tasks_path}")
    print(f"  Models file: {models_path}")
    print(f"  Tasks:       {len(tasks)} - {[t['task_id'] for t in tasks]}")
    if active_seed_conditions:
        print(f"  Seed conds:  {active_seed_conditions}")
        print(f"  Task cells:  {len(task_runs)}")
    print(f"  Models:      {len(models)} - {[m['id'] for m in models]}")
    print(f"  Variants:    {variants}")
    print(f"  Completions: {n_completions}")
    print(f"  Timeout:     {timeout}s per task")
    print(f"  Max turns:   {max_turns}")
    print(f"  System:      {system_prompt_path}")
    print(f"  Option order:{option_order_mode}")
    print(
        "  Sampling:    "
        f"temp={_format_sampling_banner(sampling.get('temperature'))}, "
        f"max_tokens={_format_sampling_banner(sampling.get('max_tokens'))}, "
        f"top_p={_format_sampling_banner(sampling.get('top_p'))}, "
        f"reasoning_effort={_format_sampling_banner(sampling.get('reasoning_effort'))}, "
        f"reasoning_by_model={_format_mapping_banner(sampling.get('reasoning_effort_by_model') or {})}, "
        f"reasoning_policy={sampling.get('reasoning_effort_policy', 'supported_only')} "
        f"[mode={sampling_mode}]"
    )
    if max_consecutive_errors > 0:
        print(f"  Fail-fast:   {max_consecutive_errors} consecutive errors per model")
    print(f"  Total runs:  {total}")
    rate_limit_delay = float(config.get("rate_limit_delay") or 0.0)
    rate_limit_delay_per_model = config.get("rate_limit_delay_per_model") or {}
    if rate_limit_delay or rate_limit_delay_per_model:
        delays = {
            model["id"]: float(rate_limit_delay_per_model.get(model["id"], rate_limit_delay) or 0.0)
            for model in models
        }
        print(
            "  Rate limit:  "
            + ", ".join(f"{model_id}={delay:g}s" for model_id, delay in delays.items())
        )
    print(f"  Env file:    {env_path}")
    print("  Credentials:")
    for model in models:
        print(f"    - {model['id']}: {', '.join(required_env_vars_for_model(model))}")
    if config.get("_source", {}).get("run_config"):
        print(f"  Config:      {config['_source']['run_config']}")
    print()

    if args.dry_run:
        print("DRY RUN:\n")
        for task in task_runs:
            for model in models:
                for variant in variants:
                    for ci in range(1, n_completions + 1):
                        print(f"  {task['task_id']} x {model['id']} x {variant} x c{ci}")
                        print(f"    Files: {task['expected_files']}")
        return

    run_dir, run_name = _resolve_run_dir(args, config)
    run_dir.mkdir(parents=True, exist_ok=True)
    config_to_save = {k: v for k, v in config.items() if not k.startswith("_")}
    config_to_save["_meta"] = config.get("_source", {})
    with open(run_dir / "config.yaml", "w") as f:
        yaml.dump(config_to_save, f, default_flow_style=False, sort_keys=False)
    if args.resume:
        print(f"  RESUMING into: {run_dir}")
    print(f"  Run directory: {run_dir}\n")

    model_jobs = {model["id"]: [] for model in models}
    for model in models:
        for task in task_runs:
            for variant in variants:
                for ci in range(1, n_completions + 1):
                    model_jobs[model["id"]].append((task, model, variant, ci))

    retry_errors = bool(config.get("retry_errors"))
    retry_empty = bool(config.get("retry_empty"))
    retry_incomplete = bool(config.get("retry_incomplete"))
    pending_model_jobs = {model_id: [] for model_id in model_jobs}
    pre_skipped = 0
    for model_id, jobs_for_model in model_jobs.items():
        for task, model, variant, ci in jobs_for_model:
            out_id = _agentic_output_id(task, variant, ci)
            out_dir = run_dir / "raw" / "agentic" / model["id"] / out_id
            if out_dir.exists() and (out_dir / "_meta.json").exists():
                if not _run_needs_retry(out_dir, task, retry_errors, retry_empty, retry_incomplete):
                    pre_skipped += 1
                    continue
            pending_model_jobs[model_id].append((task, model, variant, ci))

    pending_jobs = [job for jobs_for_model in pending_model_jobs.values() for job in jobs_for_model]
    print(f"  Scheduled:   {len(pending_jobs)} run(s)")
    if pre_skipped:
        print(f"  Pre-skipped: {pre_skipped} existing run(s)")
    print()

    completed = 0
    skipped = pre_skipped
    errors = 0
    aborted = 0
    consecutive_errors = {}
    aborted_models = set()
    lock = threading.Lock()
    start_time = time.time()

    rate_limit_delay = float(config.get("rate_limit_delay") or 0.0)
    rate_limit_delay_per_model = config.get("rate_limit_delay_per_model") or {}

    def delay_for(model_id):
        return float(rate_limit_delay_per_model.get(model_id, rate_limit_delay) or 0.0)

    def record_model_result(model_id, has_error):
        if max_consecutive_errors <= 0:
            return
        if has_error:
            n = consecutive_errors.get(model_id, 0) + 1
            consecutive_errors[model_id] = n
            if n >= max_consecutive_errors and model_id not in aborted_models:
                aborted_models.add(model_id)
                tqdm.write(
                    f"  ABORT  {model_id}: {n} consecutive errors - "
                    f"skipping remaining tasks for this model"
                )
        else:
            consecutive_errors[model_id] = 0

    async def run_job(task, model, variant, ci):
        nonlocal completed, errors, aborted
        out_id = _agentic_output_id(task, variant, ci)
        out_dir = run_dir / "raw" / "agentic" / model["id"] / out_id

        if out_dir.exists() and (out_dir / "_meta.json").exists():
            if _run_needs_retry(out_dir, task, retry_errors, retry_empty, retry_incomplete):
                shutil.rmtree(out_dir)

        if model["id"] in aborted_models:
            with lock:
                aborted += 1
            return {
                "status": "aborted",
                "task": task,
                "model": model,
                "variant": variant,
                "completion_index": ci,
                "files_found": None,
                "error": {
                    "type": "FailFastAborted",
                    "message": f"Skipped after {max_consecutive_errors} consecutive errors for {model['id']}.",
                },
            }

        # Include the run name so concurrent ablation runs do not delete each
        # other's workspaces for the same model/task/completion cell.
        workspace = Path(f"/tmp/vibench_agentic_litellm_agents/{run_name}/{model['id']}/{out_id}")
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
        result = await run_agents_sdk(
            task,
            prompt,
            workspace,
            model,
            timeout=timeout,
            max_turns=max_turns,
            system_prompt=system_prompt,
            system_prompt_path=system_prompt_path,
            sampling=sampling,
            verbose=args.verbose,
        )
        result["option_order_mode"] = option_order_mode
        result["option_order_affiliation"] = model.get("ecosystem_affiliation")
        generated_files = collect_files(workspace, task["expected_files"])
        files_found = sum(1 for value in generated_files.values() if value is not None)
        error = result["error"] or ({
            "type": "NoFilesProduced",
            "message": "Agents SDK run ended without an explicit process error, but none of the expected files were generated.",
        } if files_found == 0 else None)

        with lock:
            completed += 1
            if error:
                errors += 1
            record_model_result(model["id"], bool(error))

        _save_agentic_output(out_dir, task, model, variant, ci, result, generated_files, workspace)
        return {
            "status": "ok" if not error else "error",
            "task": task,
            "model": model,
            "variant": variant,
            "completion_index": ci,
            "files_found": files_found,
            "error": error,
            "elapsed_seconds": result["elapsed_seconds"],
        }

    async def process_model_jobs(model_id, jobs_for_model, model_pbar=None, total_pbar=None):
        for task, model, variant, ci in jobs_for_model:
            result = await run_job(task, model, variant, ci)
            if model_pbar:
                model_pbar.update(1)
                if result["status"] != "aborted":
                    model_pbar.set_postfix_str(
                        f"{_agentic_job_label(task, variant, ci)}|{result['files_found']}/{len(task['expected_files'])}|err={errors}"
                    )
            if total_pbar:
                total_pbar.update(1)
            if args.verbose:
                label = f"{task['task_id']} x {model['id']} x {variant} x c{ci}"
                if result["status"] == "aborted":
                    print(f"{label} ... ABORTED")
                elif result["error"]:
                    print(f"{label} ... ERROR: {result['error']['type']}: {result['error']['message'][:80]}")
                else:
                    print(f"{label} ... OK ({result['elapsed_seconds']}s) | {result['files_found']}/{len(task['expected_files'])} files")
            delay = delay_for(model_id)
            if delay > 0 and result["status"] != "aborted":
                await asyncio.sleep(delay)

    if pending_jobs:
        active_model_ids = [
            model_id for model_id, jobs_for_model in pending_model_jobs.items()
            if jobs_for_model
        ]
        parallel = len(active_model_ids) > 1 and not args.sequential
        max_workers = config.get("max_workers") or len(active_model_ids)
        n_workers = min(int(max_workers), len(active_model_ids)) if parallel else 1

        if parallel:
            print(f"  Async parallel: {n_workers} model worker(s) for {len(active_model_ids)} active model(s)\n")
            total_pbar = tqdm(
                total=len(pending_jobs),
                desc="Total",
                position=0,
                unit="call",
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
            )
            model_pbars = {}
            for idx, model_id in enumerate(active_model_ids, start=1):
                model_pbars[model_id] = tqdm(
                    total=len(pending_model_jobs[model_id]),
                    desc=f"  {model_id[:28]:28s}",
                    position=idx,
                    unit="call",
                    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}]",
                    leave=False,
                )

            async def run_parallel_model_workers():
                semaphore = asyncio.Semaphore(n_workers)

                async def guarded_process_model(model_id):
                    async with semaphore:
                        try:
                            await process_model_jobs(
                                model_id,
                                pending_model_jobs[model_id],
                                model_pbars[model_id],
                                total_pbar,
                            )
                            return model_id, None
                        except Exception as exc:
                            return model_id, exc

                worker_tasks = [
                    asyncio.create_task(guarded_process_model(model_id))
                    for model_id in active_model_ids
                ]
                for task_future in asyncio.as_completed(worker_tasks):
                    model_id, exc = await task_future
                    if exc is not None:
                        print(f"\n  ASYNC WORKER ERROR ({model_id}): {exc}")

            asyncio.run(run_parallel_model_workers())
            for pbar in model_pbars.values():
                pbar.close()
            total_pbar.close()
        else:
            pbar = tqdm(total=len(pending_jobs), desc="Total", unit="call")
            async def run_sequential_model_workers():
                for model_id, jobs_for_model in pending_model_jobs.items():
                    await process_model_jobs(model_id, jobs_for_model, None, pbar)
            asyncio.run(run_sequential_model_workers())
            pbar.close()

    duration = time.time() - start_time
    _write_readme(
        run_dir,
        run_name,
        tasks,
        task_runs,
        active_seed_conditions,
        models,
        variants,
        n_completions,
        sampling,
        max_turns,
        len(pending_jobs),
        completed,
        skipped,
        errors,
        aborted,
        duration,
    )

    print()
    print("=" * 60)
    print(f"Done. Completed: {completed}, Skipped: {skipped}, Errors: {errors}, Aborted: {aborted}")
    if aborted_models:
        print(f"Fail-fast hit: {', '.join(sorted(aborted_models))}")
    print(f"Duration: {duration:.1f}s")
    print(f"Run directory: {run_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
