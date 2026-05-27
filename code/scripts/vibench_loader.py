"""
VIBench — benchmark dataset loader.

Loads benchmark data from local files (default) or the Hugging Face Hub.

Usage:
    from vibench_loader import load_benchmark, load_models

    # From local files (default) — works fully offline once data is synced
    tasks = load_benchmark()
    models = load_models()

    # Force Hugging Face
    tasks = load_benchmark(source="hf")
"""

import json
from pathlib import Path

# Hugging Face benchmark dataset used when source="hf" or local files are
# unavailable. Override with hf_repo=... if needed.
HF_REPO = "vibench-emnlp26/vibench"
LOCAL_BASE = Path(__file__).resolve().parent.parent / "benchmark"
SCENARIO_ID_MAP_FILE = LOCAL_BASE / "vibench" / "scenario_id_map.json"


def _canonical_dataset_name(dataset):
    key = (dataset or "vibench").strip().lower()
    aliases = {
        "vibench": "vibench",
        "current": "vibench",
        "v3": "vibench",
    }
    if key not in aliases:
        raise ValueError(f"Unsupported dataset '{dataset}'. This repository keeps only the current 'vibench' benchmark.")
    return aliases[key]


def _load_scenario_id_map():
    """Load old->new scenario ID mapping."""
    if SCENARIO_ID_MAP_FILE.exists():
        with open(SCENARIO_ID_MAP_FILE) as f:
            return json.load(f)
    return {}


def get_scenario_id_map():
    """Public access to the scenario ID mapping (old internal -> new public)."""
    return _load_scenario_id_map()


def remap_scenario_id(old_id, id_map=None):
    """Convert internal scenario ID (e.g., S05) to public ID (e.g., S04)."""
    if id_map is None:
        id_map = _load_scenario_id_map()
    return id_map.get(old_id, old_id)


# ── Main loaders ─────────────────────────────────────────────

def load_benchmark(dataset="vibench", config="direct", source="auto",
                   local_dir=None, hf_repo=None, format="auto"):
    """Load benchmark tasks.

    Args:
        dataset: "vibench" (current)
        config: "direct" or "agentic" (vibench only)
        source: "auto" (try local then HF), "hf", or "local"
        local_dir: override local directory path
        hf_repo: override HuggingFace repo ID
        format: "auto", "flat" (per-prompt rows for HF viewer),
                or "tasks" (per-scenario with nested subtasks for runners/server)

    Returns:
        list of task dicts
    """
    dataset = _canonical_dataset_name(dataset)

    # Default format: "tasks" for local, "flat" for HF
    if format == "auto":
        fmt = "flat" if source == "hf" else "tasks"
    else:
        fmt = format

    repo = hf_repo or HF_REPO
    if source == "auto":
        try:
            return _load_vibench_local(config, local_dir)
        except Exception:
            return _load_vibench_hf(repo, config, fmt)
    elif source == "hf":
        return _load_vibench_hf(repo, config, fmt)
    else:
        return _load_vibench_local(config, local_dir)


def load_models(dataset="vibench", source="auto", local_dir=None, hf_repo=None):
    """Load model definitions."""
    dataset = _canonical_dataset_name(dataset)
    repo = hf_repo or HF_REPO
    fname = "models.json"
    local_path = LOCAL_BASE / "vibench" / "models.json"

    if source == "auto":
        try:
            return _load_json_local(local_path)
        except Exception:
            return _load_json_hf(repo, fname)
    elif source == "hf":
        return _load_json_hf(repo, fname)
    else:
        return _load_json_local(local_path)


def load_system_prompt(dataset="vibench", prompt_type="direct", source="auto",
                       local_dir=None, hf_repo=None):
    """Load system prompt text."""
    dataset = _canonical_dataset_name(dataset)
    repo = hf_repo or HF_REPO
    fname = "agentic_system_prompt.txt" if prompt_type == "agentic" else "system_prompt.txt"
    local_path = LOCAL_BASE / "vibench" / fname

    if source == "auto":
        try:
            return local_path.read_text().strip()
        except Exception:
            return _load_text_hf(repo, fname)
    elif source == "hf":
        return _load_text_hf(repo, fname)
    else:
        return local_path.read_text().strip()


# ── HuggingFace loaders ──────────────────────────────────────

def _load_vibench_hf(repo, config, fmt="flat"):
    from huggingface_hub import hf_hub_download
    if fmt == "tasks":
        # Full task-level JSONL (nested subtasks, provider_tools, etc.)
        fname = f"tasks_{config}.jsonl"
    else:
        # Flattened per-prompt/per-scenario rows (for HF viewer)
        fname = f"{config}.jsonl"
    path = hf_hub_download(repo_id=repo, filename=fname, repo_type="dataset")
    return _read_jsonl(path)


def _load_json_hf(repo, fname):
    from huggingface_hub import hf_hub_download
    path = hf_hub_download(repo_id=repo, filename=fname, repo_type="dataset")
    with open(path) as f:
        return json.load(f)


def _load_text_hf(repo, fname):
    from huggingface_hub import hf_hub_download
    path = hf_hub_download(repo_id=repo, filename=fname, repo_type="dataset")
    return Path(path).read_text().strip()


# ── Local loaders ────────────────────────────────────────────

def _load_vibench_local(config, local_dir):
    d = Path(local_dir) if local_dir else LOCAL_BASE / "vibench"
    if config == "agentic":
        return _read_jsonl(d / "agentic" / "tasks.jsonl")
    else:
        return _read_jsonl(d / "direct" / "tasks.jsonl")


def _load_json_local(path):
    with open(path) as f:
        return json.load(f)


# ── Utilities ────────────────────────────────────────────────

def _read_jsonl(path):
    records = []
    with open(path) as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


# ── CLI ──────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="VIBench dataset loader")
    parser.add_argument("--dataset", default="vibench", choices=["vibench", "current", "v3"])
    parser.add_argument("--config", default="direct", choices=["direct", "agentic"])
    parser.add_argument("--source", default="auto", choices=["auto", "hf", "local"])
    args = parser.parse_args()

    tasks = load_benchmark(dataset=args.dataset, config=args.config, source=args.source)
    models = load_models(dataset=args.dataset, source=args.source)
    prompt = load_system_prompt(dataset=args.dataset, source=args.source)

    print(f"VIBench loaded ({args.dataset}/{args.config}, source={args.source})")
    print(f"  Tasks: {len(tasks)}")
    print(f"  Models: {len(models.get('models', []))}")
    print(f"  System prompt: {len(prompt)} chars")

    if args.dataset == "vibench":
        id_map = get_scenario_id_map()
        print(f"  Scenario ID map: {len(id_map)} entries")
        print(f"  Example: S05 (internal) -> {remap_scenario_id('S05')} (public)")
