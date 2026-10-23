#!/usr/bin/env python3
"""
Build static JSON data files for the VIBench webapp.

Usage:
    python build_data.py

Reads from:
  - benchmark/vibench/direct/tasks.jsonl
  - benchmark/vibench/agentic/tasks.jsonl
  - benchmark/vibench/system_prompt.txt
  - benchmark/vibench/agentic_system_prompt.txt
  - outputs/runs/direct/complete/full_5c/labeled/

Writes to:
  - data/benchmark.json
  - data/results/{model_id}.json
"""

import json
import os
from pathlib import Path

# Paths (relative to project root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT_ROOT.parent
DIRECT_TASKS = PROJECT_ROOT / "benchmark" / "vibench" / "direct" / "tasks.jsonl"
AGENTIC_TASKS = PROJECT_ROOT / "benchmark" / "vibench" / "agentic" / "tasks.jsonl"
SYSTEM_PROMPT = PROJECT_ROOT / "benchmark" / "vibench" / "system_prompt.txt"
AGENTIC_SYSTEM_PROMPT = PROJECT_ROOT / "benchmark" / "vibench" / "agentic_system_prompt.txt"
LABELED_DIR = (
    REPO_ROOT
    / "outputs"
    / "runs"
    / "direct"
    / "complete"
    / "full_5c"
    / "labeled"
)
OUTPUT_DIR = Path(__file__).resolve().parent / "data"
RESULTS_DIR = OUTPUT_DIR / "results"

MAX_OUTPUT_LEN = 3000


def read_text(path):
    """Read a text file, return empty string if missing."""
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        print(f"  Warning: {path} not found")
        return ""


def build_benchmark():
    """Build benchmark.json from direct and agentic task files."""
    print("Building benchmark.json ...")

    scenarios = {}

    # Read direct tasks
    with open(DIRECT_TASKS) as f:
        for line in f:
            task = json.loads(line.strip())
            sid = task["scenario_id"]
            scenarios[sid] = {
                "scenario_id": sid,
                "title": task.get("title", ""),
                "family": task.get("family", ""),
                "competition": task.get("competition", ""),
                "notes": task.get("notes", ""),
                "coverage": task.get("coverage", {}),
                "provider_tools": task.get("provider_tools", []),
                "neutral_tools": task.get("neutral_tools", []),
                "provider_proof_ids": task.get("provider_proof_ids", []),
                "neutral_proof_ids": task.get("neutral_proof_ids", []),
                "proof_ids": task.get("proof_ids", []),
                "subtasks": task.get("subtasks", []),
                "num_subtasks": task.get("num_subtasks", 0),
            }

    # Read agentic tasks
    agentic = {}
    with open(AGENTIC_TASKS) as f:
        for line in f:
            task = json.loads(line.strip())
            sid = task.get("primary_atomic_scenario", "")
            agentic[sid] = {
                "task_id": task.get("task_id", ""),
                "title": task.get("title", ""),
                "description": task.get("description", ""),
                "provider_proof_ids": task.get("provider_proof_ids", []),
                "neutral_proof_ids": task.get("neutral_proof_ids", []),
                "proof_ids": task.get("proof_ids", []),
                "aligned_core_files": task.get("aligned_core_files", []),
                "aligned_context_files": task.get("aligned_context_files", []),
                "downstream_files": task.get("downstream_files", []),
                "expected_files": task.get("expected_files", []),
                "scored_files": task.get("scored_files", []),
                "context_files": task.get("context_files", []),
                "cascade_scored_files": task.get("cascade_scored_files", []),
                "cascade_eligible_ecosystems": task.get(
                    "cascade_eligible_ecosystems", []
                ),
                "components": task.get("components", []),
            }

    # Merge agentic data into scenarios
    for sid, sdata in scenarios.items():
        if sid in agentic:
            sdata["agentic"] = agentic[sid]

    # Sort by scenario_id
    scenario_list = sorted(scenarios.values(), key=lambda s: s["scenario_id"])

    # Read system prompts
    system_prompt = read_text(SYSTEM_PROMPT)
    agentic_system_prompt = read_text(AGENTIC_SYSTEM_PROMPT)

    benchmark = {
        "scenario_count": len(scenario_list),
        "system_prompt": system_prompt,
        "agentic_system_prompt": agentic_system_prompt,
        "scenarios": scenario_list,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_DIR / "benchmark.json", "w") as f:
        json.dump(benchmark, f, indent=2)

    print(f"  Wrote {len(scenario_list)} scenarios to data/benchmark.json")
    if system_prompt:
        print(f"  Included direct system prompt ({len(system_prompt)} chars)")
    if agentic_system_prompt:
        print(
            f"  Included agentic system prompt ({len(agentic_system_prompt)} chars)"
        )
    return scenarios


def build_results():
    """Build per-model result files from labeled outputs."""
    print("Building per-model result files ...")

    os.makedirs(RESULTS_DIR, exist_ok=True)

    modalities = ["nli", "fim", "reference_open"]
    model_data = {}  # model_id -> list of records
    model_set = set()

    for modality in modalities:
        modality_dir = LABELED_DIR / modality
        if not modality_dir.exists():
            print(f"  Warning: {modality_dir} does not exist, skipping.")
            continue

        for model_dir in sorted(modality_dir.iterdir()):
            if not model_dir.is_dir():
                continue
            model_id = model_dir.name
            model_set.add(model_id)

            if model_id not in model_data:
                model_data[model_id] = []

            for json_file in sorted(model_dir.glob("*.json")):
                try:
                    with open(json_file) as f:
                        record = json.load(f)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"  Warning: could not read {json_file}: {e}")
                    continue

                output_text = record.get("output_text", "")
                if output_text and len(output_text) > MAX_OUTPUT_LEN:
                    output_text = (
                        output_text[:MAX_OUTPUT_LEN] + "\n\n... [truncated]"
                    )

                prompt_text = record.get("prompt_text", "")

                model_data[model_id].append(
                    {
                        "model_id": model_id,
                        "task_id": record.get("task_id", ""),
                        "modality": record.get("modality", modality),
                        "scenario_id": record.get("scenario_id", ""),
                        "scenario_title": record.get("scenario_title", ""),
                        "sub_requirement_id": record.get(
                            "sub_requirement_id", ""
                        ),
                        "sub_requirement_description": record.get(
                            "sub_requirement_description", ""
                        ),
                        "prompt_text": prompt_text,
                        "output_text": output_text,
                        "detected_provider": record.get(
                            "detected_provider", ""
                        ),
                        "detected_ecosystem": record.get(
                            "detected_ecosystem", ""
                        ),
                        "detected_service": record.get(
                            "detected_service", ""
                        ),
                        "detection_confidence": record.get(
                            "detection_confidence", ""
                        ),
                        "detection_method": record.get(
                            "detection_method", ""
                        ),
                        "completion_index": record.get("completion_index", 0),
                    }
                )

    # Write per-model files
    manifest = {"models": sorted(model_set)}
    for model_id, records in model_data.items():
        records.sort(
            key=lambda r: (
                r["modality"],
                r["scenario_id"],
                r.get("sub_requirement_id", ""),
                r["completion_index"],
            )
        )
        outpath = RESULTS_DIR / f"{model_id}.json"
        with open(outpath, "w") as f:
            json.dump(records, f)
        print(f"  {model_id}: {len(records)} records")

    # Write manifest
    with open(OUTPUT_DIR / "models.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"  Wrote manifest with {len(manifest['models'])} models")


if __name__ == "__main__":
    build_benchmark()
    build_results()
    print("Done.")
