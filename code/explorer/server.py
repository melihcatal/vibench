#!/usr/bin/env python3
"""
VIBench Explorer — dynamic Flask server.

Usage:
    python server.py              # starts on http://localhost:5050
    python server.py --port 8080  # custom port

Reads directly from:
  - benchmark/vibench/direct/tasks.jsonl
  - benchmark/vibench/agentic/tasks.jsonl
  - benchmark/vibench/system_prompt.txt
  - benchmark/vibench/agentic_system_prompt.txt
  - outputs/runs/**/labeled/
  - vibench-explorer/evaluations.json  (persisted evaluations)
"""

import argparse
import copy
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

from flask import Flask, jsonify, request, send_file, send_from_directory

# Add scripts dir to path for vibench_loader
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

# ── Paths ────────────────────────────────────────────────────

# code/ holds the benchmark corpus, scripts and validation files; the generated
# outputs sit beside it at the repository root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT_ROOT.parent
WEBAPP_DIR = Path(__file__).resolve().parent

DIRECT_TASKS = PROJECT_ROOT / "benchmark" / "vibench" / "direct" / "tasks.jsonl"
AGENTIC_TASKS = PROJECT_ROOT / "benchmark" / "vibench" / "agentic" / "tasks.jsonl"
SYSTEM_PROMPT = PROJECT_ROOT / "benchmark" / "vibench" / "system_prompt.txt"
AGENTIC_SYSTEM_PROMPT = PROJECT_ROOT / "benchmark" / "vibench" / "agentic_system_prompt.txt"

# Every run lives under outputs/runs/; there is no second "curated" tier.
RUN_SEARCH_DIRS = [REPO_ROOT / "outputs" / "runs"]
EVAL_FILE = WEBAPP_DIR / "evaluations.json"
RESULTS_SUMMARY_FILE = (REPO_ROOT / "outputs" / "runs" / "direct" / "complete"
                        / "full_5c" / "report.md")
FIGURES_DIR = REPO_ROOT / "figures"

HF_BENCHMARK_REPO = os.environ.get("VIBENCH_HF_BENCHMARK_REPO", "vibench-emnlp26/vibench")
HF_RESULTS_REPO = os.environ.get("VIBENCH_HF_RESULTS_REPO", "vibench-emnlp26/vibench-results")
RESULTS_SOURCE = os.environ.get("VIBENCH_RESULTS_SOURCE", "auto")
_HF_RESULTS_ROOT = None
_HF_RESULTS_INDEX = None
_BENCHMARK_PROOF_INDEX = None

MAX_OUTPUT_LEN = 4000

# ── Flask app ────────────────────────────────────────────────

app = Flask(__name__, static_folder=str(WEBAPP_DIR), static_url_path="")


def _repo_rel(path):
    """A path as the repository shows it, whichever root it sits under.

    Raises ValueError for a path under neither root, like relative_to does:
    callers use that to label external files.
    """
    path = Path(path)
    for base in (REPO_ROOT, PROJECT_ROOT):
        try:
            return str(path.relative_to(base))
        except ValueError:
            continue
    raise ValueError(f"{path} is outside the repository")


def read_text(path):
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return ""


def _read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _read_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


# ── Static files ─────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(str(WEBAPP_DIR), "index.html")


@app.route("/figures/<path:filename>")
def figures(filename):
    root = _figure_root()
    return send_from_directory(str(root), filename)


def _benchmark_evidence_artifact_path(relpath: str) -> Path:
    safe = Path(relpath)
    if safe.is_absolute() or ".." in safe.parts:
        raise FileNotFoundError(relpath)
    local_path = PROJECT_ROOT / "benchmark" / "vibench" / "evidence" / safe
    if BENCHMARK_SOURCE != "hf" and local_path.exists():
        return local_path
    from huggingface_hub import hf_hub_download

    filename = str(Path("evidence") / safe).replace("\\", "/")
    return Path(
        hf_hub_download(
            repo_id=HF_BENCHMARK_REPO,
            repo_type="dataset",
            filename=filename,
        )
    )


@app.route("/benchmark-evidence/<path:filename>")
def benchmark_evidence(filename):
    try:
        path = _benchmark_evidence_artifact_path(filename)
    except Exception:
        return "Not found", 404
    if not path.exists():
        return "Not found", 404
    return send_file(path)


@app.route("/<path:filename>")
def static_files(filename):
    # Only serve known static extensions
    if filename.endswith((".html", ".css", ".js", ".ico", ".png", ".svg")):
        return send_from_directory(str(WEBAPP_DIR), filename)
    return "Not found", 404


# ── API: Benchmark data ─────────────────────────────────────

BENCHMARK_SOURCE = "auto"  # overridable via --benchmark-source


def _snapshot_hf_results():
    """Download/cache explicit HF result metadata files and return a local root.

    Raw agentic files are intentionally excluded here. They are fetched lazily
    by `/api/result-detail` so opening the explorer does not request tens of
    thousands of small files from Hugging Face.
    """
    global _HF_RESULTS_ROOT
    if _HF_RESULTS_ROOT is not None:
        return _HF_RESULTS_ROOT
    from huggingface_hub import hf_hub_download

    cache_root = (
        Path(tempfile.gettempdir())
        / "vibench_hf_results"
        / HF_RESULTS_REPO.replace("/", "--")
    )
    files = [
        "manifest.json",
        "README.md",
        "docs/results/current_results.md",
        "docs/figures/agentic/claude_agentic_heatmap.png",
        "docs/figures/agentic/claude_forest_agentic.png",
        "docs/figures/ablations/claude_option_order_with_main.png",
        "docs/figures/ablations/claude_agents_sdk_vs_opencode.png",
        "docs/figures/cascade/claude_cascade_leakage.png",
        "docs/figures/combined/claude_combined_vib.png",
        "docs/figures/combined/claude_dumbbell_effectsize.png",
        "docs/figures/direct/claude_direct_heatmap.png",
        "docs/figures/direct/claude_forest_direct.png",
        "docs/figures/examples/claude_direct_consensus_example.png",
        "docs/figures/modality/claude_modality_comparison.png",
        "docs/figures/scenario/claude_scenario_matrix.png",
        "docs/figures/transition/claude_transition_arrow.png",
        "docs/figures/transition/claude_transition_arrow_refopen_informed.png",
        "vibench-explorer/data/results_index.json",
        "vibench-explorer/data/benchmark.json",
        "vibench-explorer/data/models.json",
    ]
    for filename in files:
        try:
            src = Path(
                hf_hub_download(
                    repo_id=HF_RESULTS_REPO,
                    repo_type="dataset",
                    filename=filename,
                )
            )
        except Exception:
            # Only the index, manifest, and current report are required.
            if filename in {
                "manifest.json",
                "docs/results/current_results.md",
                "vibench-explorer/data/results_index.json",
            }:
                raise
            continue
        dst = cache_root / filename
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dst)
    _HF_RESULTS_ROOT = cache_root
    return _HF_RESULTS_ROOT


def _figure_root():
    if RESULTS_SOURCE == "hf" or (RESULTS_SOURCE == "auto" and not FIGURES_DIR.exists()):
        try:
            candidate = _snapshot_hf_results() / "docs" / "figures"
            if candidate.exists():
                return candidate
        except Exception as e:
            print(f"  HF figure load failed: {e}, falling back to local")
    return FIGURES_DIR


def _load_hf_results_index():
    global _HF_RESULTS_INDEX
    if RESULTS_SOURCE not in ("hf", "auto"):
        return None
    if RESULTS_SOURCE == "auto" and _local_results_available():
        return None
    if _HF_RESULTS_INDEX is not None:
        return _HF_RESULTS_INDEX
    try:
        index_path = _snapshot_hf_results() / "vibench-explorer" / "data" / "results_index.json"
        if index_path.exists():
            _HF_RESULTS_INDEX = json.loads(index_path.read_text(encoding="utf-8"))
            return _HF_RESULTS_INDEX
    except Exception as e:
        print(f"  HF results index load failed: {e}")
    return None


def _local_results_available():
    return any((REPO_ROOT / "outputs" / "runs").rglob("labeled"))


def _result_search_dirs():
    """Return local and/or HF-backed roots that contain labeled run folders."""
    if RESULTS_SOURCE == "local":
        return RUN_SEARCH_DIRS

    if RESULTS_SOURCE == "hf" or (RESULTS_SOURCE == "auto" and not _local_results_available()):
        try:
            root = _snapshot_hf_results()
            return [root / "outputs" / "runs", root / "results"]
        except Exception as e:
            print(f"  HF results load failed: {e}, falling back to local")

    return RUN_SEARCH_DIRS


def _summary_markdown_path():
    if RESULTS_SOURCE == "hf" or (RESULTS_SOURCE == "auto" and not RESULTS_SUMMARY_FILE.exists()):
        try:
            candidate = _snapshot_hf_results() / "docs" / "results" / "current_results.md"
            if candidate.exists():
                return candidate, "hf"
        except Exception as e:
            print(f"  HF summary load failed: {e}, falling back to local")
    return RESULTS_SUMMARY_FILE, "local"


def _load_results_manifest():
    for root in _result_search_dirs():
        manifest = root.parent.parent / "manifest.json" if root.name == "runs" else root / "manifest.json"
        if manifest.exists():
            try:
                return json.loads(manifest.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, IOError):
                pass
    if RESULTS_SOURCE == "hf":
        try:
            manifest = _snapshot_hf_results() / "manifest.json"
            if manifest.exists():
                return json.loads(manifest.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _load_prompt(prompt_type):
    local_path = AGENTIC_SYSTEM_PROMPT if prompt_type == "agentic" else SYSTEM_PROMPT
    if BENCHMARK_SOURCE == "hf" or (BENCHMARK_SOURCE == "auto" and not local_path.exists()):
        try:
            from vibench_loader import load_system_prompt

            return load_system_prompt(
                prompt_type=prompt_type,
                source="hf",
                hf_repo=HF_BENCHMARK_REPO,
            )
        except Exception as e:
            print(f"  HF prompt load failed: {e}, falling back to local")
    return read_text(local_path)


def _load_tasks_from_source():
    """Load tasks from local files or HuggingFace.

    Returns task-level objects (one per scenario with nested subtasks).
    """
    if BENCHMARK_SOURCE == "hf" or (BENCHMARK_SOURCE == "auto" and not DIRECT_TASKS.exists()):
        try:
            from vibench_loader import load_benchmark
            direct = load_benchmark(config="direct", source="hf", hf_repo=HF_BENCHMARK_REPO, format="tasks")
            agentic = load_benchmark(config="agentic", source="hf", hf_repo=HF_BENCHMARK_REPO, format="tasks")
            return direct + agentic
        except Exception as e:
            print(f"  HF load failed: {e}, falling back to local")

    tasks = []
    if DIRECT_TASKS.exists():
        with open(DIRECT_TASKS) as f:
            for line in f:
                if line.strip():
                    tasks.append(json.loads(line.strip()))
    if AGENTIC_TASKS.exists():
        with open(AGENTIC_TASKS) as f:
            for line in f:
                if line.strip():
                    tasks.append(json.loads(line.strip()))
    return tasks


def _load_benchmark_proof_index():
    global _BENCHMARK_PROOF_INDEX
    if _BENCHMARK_PROOF_INDEX is not None:
        return _BENCHMARK_PROOF_INDEX

    try:
        registry = _read_jsonl(_benchmark_evidence_artifact_path("registry/proofs.jsonl"))
        snapshots = _read_json(_benchmark_evidence_artifact_path("generated/provider_doc_snapshots.json"))
        quality = _read_json(_benchmark_evidence_artifact_path("generated/provider_doc_snapshot_quality.json"))
    except Exception as e:
        print(f"  Benchmark evidence load failed: {e}")
        _BENCHMARK_PROOF_INDEX = {}
        return _BENCHMARK_PROOF_INDEX

    proofs_by_id = {}
    for row in registry:
        proof_id = row.get("proof_id")
        if not proof_id:
            continue
        proofs_by_id[proof_id] = {
            "proof_id": proof_id,
            "url": row.get("url"),
            "title": row.get("title"),
            "titles": row.get("titles", []),
            "domain": row.get("domain"),
            "scenario_ids": row.get("scenario_ids", []),
            "provider_keys": row.get("provider_keys", []),
            "roles": row.get("roles", []),
        }

    for row in snapshots:
        proof_id = row.get("proof_id")
        if not proof_id or proof_id not in proofs_by_id:
            continue
        proofs_by_id[proof_id].update(
            {
                "snapshot_relpath": row.get("snapshot_relpath"),
                "snapshot_href": f"/benchmark-evidence/{row['snapshot_relpath']}"
                if row.get("snapshot_relpath")
                else None,
                "snapshot_http_status": row.get("http_status"),
                "snapshot_content_type": row.get("content_type"),
                "snapshot_capture_method": row.get("capture_method"),
                "snapshot_final_url": row.get("final_url"),
                "snapshot_sha256": row.get("sha256"),
            }
        )

    for row in quality:
        proof_id = row.get("proof_id")
        if not proof_id or proof_id not in proofs_by_id:
            continue
        proofs_by_id[proof_id].update(
            {
                "snapshot_quality": row.get("quality"),
                "snapshot_flags": row.get("flags", []),
                "snapshot_title": row.get("title"),
                "snapshot_h1": row.get("h1"),
                "snapshot_visible_excerpt": row.get("visible_excerpt"),
            }
        )

    _BENCHMARK_PROOF_INDEX = proofs_by_id
    return _BENCHMARK_PROOF_INDEX


@app.route("/api/benchmark")
def api_benchmark():
    """Return full benchmark data (scenarios + system prompts)."""
    all_tasks = _load_tasks_from_source()
    scenarios = {}

    for task in all_tasks:
        stage = task.get("stage", task.get("dataset_kind", "direct"))
        if "agentic" in stage:
            sid = task.get("primary_atomic_scenario", "")
            if sid in scenarios:
                scenarios[sid]["agentic"] = {
                    "task_id": task.get("task_id", ""),
                    "title": task.get("title", ""),
                    "description": task.get("description", ""),
                    "aligned_core_files": task.get("aligned_core_files", []),
                    "aligned_context_files": task.get("aligned_context_files", []),
                    "downstream_files": task.get("downstream_files", []),
                    "expected_files": task.get("expected_files", []),
                    "scored_files": task.get("scored_files", []),
                    "context_files": task.get("context_files", []),
                    "cascade_scored_files": task.get("cascade_scored_files", []),
                    "cascade_eligible_ecosystems": task.get("cascade_eligible_ecosystems", []),
                    "components": task.get("components", []),
                }
        else:
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
                "subtasks": task.get("subtasks", []),
                "num_subtasks": task.get("num_subtasks", 0),
            }

    scenario_list = sorted(scenarios.values(), key=lambda s: s["scenario_id"])

    return jsonify({
        "scenario_count": len(scenario_list),
        "system_prompt": _load_prompt("direct"),
        "agentic_system_prompt": _load_prompt("agentic"),
        "proofs_by_id": _load_benchmark_proof_index(),
        "scenarios": scenario_list,
    })


# ── Computed study totals ────────────────────────────────────

# Nothing here is hardcoded: the explorer counts what is actually shipped, so a
# pruned or extended checkout reports its own contents rather than stale copy.

_RAW_FILE_COUNT = None
_STUDY_TOTALS = None


def _raw_file_count():
    """Generated files across the runs. Walks ~96k paths, so compute it once."""
    global _RAW_FILE_COUNT
    if _RAW_FILE_COUNT is None:
        _RAW_FILE_COUNT = sum(
            1
            for root in _result_search_dirs()
            if root.exists()
            for path in root.glob("**/raw/**/*")
            if path.is_file()
        )
    return _RAW_FILE_COUNT


_LABELED_COUNTS = {}


def _count_labeled(run_dir):
    """Labeled records in one run: per-file JSON for direct, session rows for agentic.

    Counting a direct run means walking a few thousand files, and the ablation
    and summary views ask for every run at once, so memoise it.
    """
    key = str(run_dir)
    cached = _LABELED_COUNTS.get(key)
    if cached is not None:
        return cached
    agentic = run_dir / "labeled" / "agentic" / "results.json"
    if agentic.exists():
        try:
            count = len(_read_json(agentic))
        except Exception:
            count = 0
    else:
        count = sum(1 for _ in (run_dir / "labeled").rglob("*.json"))
    _LABELED_COUNTS[key] = count
    return count


def _study_totals():
    global _STUDY_TOTALS
    if _STUDY_TOTALS is not None:
        return _STUDY_TOTALS
    runs_root = REPO_ROOT / "outputs" / "runs"
    totals = {"direct_main": 0, "direct_ablation": 0, "agentic_main": 0,
              "agentic_ablation": 0, "agents_sdk": 0, "runs": 0}
    for labeled in sorted(runs_root.rglob("labeled")):
        if not labeled.is_dir():
            continue
        run = labeled.parent
        rel = run.relative_to(runs_root).as_posix()
        n = _count_labeled(run)
        totals["runs"] += 1
        agentic = (run / "labeled" / "agentic").is_dir()
        if "variants/" in rel:
            totals["agentic_ablation" if agentic else "direct_ablation"] += n
        elif "agents_sdk" in rel:
            totals["agents_sdk"] += n
        elif agentic:
            totals["agentic_main"] += n
        else:
            totals["direct_main"] += n
    totals["ablation"] = totals["direct_ablation"] + totals["agentic_ablation"]
    totals["indexed"] = (totals["direct_main"] + totals["agentic_main"]
                         + totals["agents_sdk"] + totals["ablation"])
    _STUDY_TOTALS = totals
    return totals


_VIB_LINE = re.compile(
    r"^\s*(\S+)\s+→\s*(\S+)\s*:\s*VIB = ([+-][\d.]+)%\s*"
    r"\(self=([\d.]+)%, ctrl=([\d.]+)%")


def _direct_vib_rows():
    """VIB per model, parsed from the report `make evaluate` regenerates."""
    report = (REPO_ROOT / "outputs" / "runs" / "direct" / "complete"
              / "full_5c" / "report.md")
    rows = []
    if not report.exists():
        return rows
    for line in report.read_text(encoding="utf-8").splitlines():
        m = _VIB_LINE.match(line)
        if m:
            rows.append({"model": m.group(1), "ecosystem": m.group(2),
                         "vib": float(m.group(3)), "self_rate": float(m.group(4)),
                         "control_rate": float(m.group(5))})
    rows.sort(key=lambda r: -r["vib"])
    return rows


@app.route("/api/summary")
def api_summary():
    """Return the current paper-facing result summary."""
    path, source = _summary_markdown_path()
    markdown = read_text(path)
    runs = _discover_runs()
    manifest = _load_results_manifest()
    raw_file_count = manifest.get("raw_files")
    if raw_file_count is None:
        raw_file_count = _raw_file_count()
    totals = _study_totals()
    vib_rows = _direct_vib_rows()
    metrics = [
        {
            "label": "Indexed labeled records",
            "value": f"{totals['indexed']:,}",
            "detail": (f"{totals['direct_main']:,} direct + "
                       f"{totals['agentic_main']:,} agentic + "
                       f"{totals['agents_sdk']:,} runtime check + "
                       f"{totals['ablation']:,} ablation, across {totals['runs']} runs"),
        },
        {
            "label": "Main direct generations",
            "value": f"{totals['direct_main']:,}",
            "detail": "every study model x scenario x subtask x prompt variant x completion",
        },
        {
            "label": "Main agentic sessions",
            "value": f"{totals['agentic_main']:,}",
            "detail": f"plus {totals['agents_sdk']:,} on the second agent runtime",
        },
        {
            "label": "Ablation records",
            "value": f"{totals['ablation']:,}",
            "detail": (f"{totals['direct_ablation']:,} direct + "
                       f"{totals['agentic_ablation']:,} agentic config variants"),
        },
    ]
    if vib_rows:
        top = vib_rows[0]
        positive = [r for r in vib_rows if r["vib"] > 0]
        metrics.insert(0, {
            "label": "Strongest direct VIB",
            "value": f"{top['vib']:+.1f}pp",
            "detail": (f"{top['model']} → {top['ecosystem']}: "
                       f"self {top['self_rate']:.1f}% vs control {top['control_rate']:.1f}%"),
        })
        metrics.insert(1, {
            "label": "Affiliated models with positive VIB",
            "value": f"{len(positive)}/{len(vib_rows)}",
            "detail": "computed from the direct evaluation report",
        })
    return jsonify({
        "source": source,
        "path": str(path),
        "markdown": markdown,
        "metrics": metrics,
        "runs": [
            {
                "run_id": run["run_id"],
                "source": run["source"],
            }
            for run in runs
        ],
    })


# ── API: Models manifest ────────────────────────────────────

def _discover_runs():
    """Find all labeled run directories."""
    index = _load_hf_results_index()
    if index:
        root = _snapshot_hf_results()
        return [
            {
                "run_id": run["run_id"],
                "path": root / "outputs" / "runs" / run["run_id"] / "labeled",
                "run_root": root / "outputs" / "runs" / run["run_id"],
                "source": "hf",
                "has_direct": run.get("has_direct", False),
                "has_agentic": run.get("has_agentic", False),
                "hf_index": True,
            }
            for run in index.get("runs", [])
        ]

    runs = list(_campaign_run_index())
    seen = {r["run_id"] for r in runs}
    for base_dir in _result_search_dirs():
        if not base_dir.exists():
            continue
        for labeled in sorted(base_dir.rglob("labeled")):
            if not labeled.is_dir():
                continue
            run_dir = labeled.parent
            try:
                run_id = run_dir.relative_to(base_dir).as_posix()
            except ValueError:
                run_id = run_dir.name
            if run_id in seen:
                continue
            seen.add(run_id)
            try:
                source = _repo_rel(base_dir)
            except ValueError:
                source = str(base_dir)
            runs.append({
                "run_id": run_id,
                "path": labeled,
                "run_root": run_dir,
                "source": source,
            })
    return runs


def _filter_runs(run_ids=None):
    runs = _discover_runs()
    if not run_ids:
        return runs
    wanted = set(run_ids)
    return [r for r in runs if r["run_id"] in wanted]


def _parse_csv_arg(name):
    raw = request.args.get(name, "")
    return [v.strip() for v in raw.split(",") if v.strip()]


def _is_hf_run(run):
    if _HF_RESULTS_ROOT is None:
        return False
    try:
        Path(run["run_root"]).resolve().relative_to(_HF_RESULTS_ROOT.resolve())
        return True
    except ValueError:
        return False


def _hf_result_file_text(repo_path):
    """Download one file from the private HF results repo and return text."""
    from huggingface_hub import hf_hub_download

    path = hf_hub_download(
        repo_id=HF_RESULTS_REPO,
        repo_type="dataset",
        filename=repo_path,
    )
    return Path(path).read_text(encoding="utf-8")


def _raw_agentic_repo_path(run, model_id, session_key, filename):
    return f"outputs/runs/{run['run_id']}/raw/agentic/{model_id}/{session_key}/{filename}"


def _read_agentic_raw_file(run, local_session_dir, model_id, session_key, filename):
    local_path = local_session_dir / filename
    if local_path.exists():
        try:
            return local_path.read_text(encoding="utf-8")
        except IOError:
            return ""
    if _is_hf_run(run):
        try:
            return _hf_result_file_text(
                _raw_agentic_repo_path(run, model_id, session_key, filename)
            )
        except Exception as e:
            print(f"  HF raw file load failed for {filename}: {e}")
    return ""


def _discover_models(run_ids=None):
    """Discover all model IDs across selected runs."""
    index = _load_hf_results_index()
    if index:
        wanted = set(run_ids or [])
        return sorted({
            rec.get("model_id", "")
            for rec in index.get("records", [])
            if rec.get("model_id") and (not wanted or rec.get("run_id") in wanted)
        })

    models = set()
    for run in _filter_runs(run_ids):
        if run.get("campaign"):
            models.update(c["model"] for c in _campaign_cells(run["run_root"]))
            continue
        labeled = run["path"]
        for modality in ["nli", "fim", "reference_open"]:
            modality_dir = labeled / modality
            if not modality_dir.is_dir():
                continue
            for model_dir in modality_dir.iterdir():
                if model_dir.is_dir():
                    models.add(model_dir.name)
        agentic_results = labeled / "agentic" / "results.json"
        if agentic_results.exists():
            try:
                data = json.loads(agentic_results.read_text())
                if isinstance(data, list):
                    models.update(r.get("model_id", "") for r in data if r.get("model_id"))
            except (json.JSONDecodeError, IOError):
                pass
    return sorted(models)


@app.route("/api/runs")
def api_runs():
    """Return discovered labeled runs."""
    runs = []
    for run in _discover_runs():
        runs.append({
            "run_id": run["run_id"],
            "source": run["source"],
            "has_direct": run.get(
                "has_direct",
                any((run["path"] / m).is_dir() for m in ["nli", "fim", "reference_open"]),
            ),
            "has_agentic": run.get(
                "has_agentic",
                (run["path"] / "agentic" / "results.json").exists(),
            ),
        })
    return jsonify({"runs": runs})


@app.route("/api/models")
def api_models():
    """Return list of available models."""
    return jsonify({"models": _discover_models(_parse_csv_arg("run"))})


# ── API: Results for a model (lightweight list) ──────────────

def _build_agentic_index(run, model_id):
    """Build index of agentic sessions for a model (lightweight, no file contents)."""
    records = []
    labeled = run["path"]
    agentic_results = labeled / "agentic" / "results.json"
    agentic_raw_dir = labeled.parent / "raw" / "agentic" / model_id
    if not agentic_results.exists():
        return records

    try:
        with open(agentic_results) as f:
            all_agentic = json.load(f)
        if not isinstance(all_agentic, list):
            return records

        for lm in all_agentic:
            if lm.get("model_id") != model_id:
                continue
            task_id = lm.get("task_id", "")
            variant = lm.get("variant", "free")
            completion_index = lm.get("completion_index", 1)
            sess_key = f"{task_id}__{variant}__c{completion_index}"
            session_dir = agentic_raw_dir / sess_key
            meta = {}
            meta_file = session_dir / "_meta.json"
            if meta_file.exists():
                try:
                    with open(meta_file) as f:
                        meta = json.load(f)
                except (json.JSONDecodeError, IOError):
                    meta = {}
            if session_dir.is_dir():
                n_files = sum(1 for p in session_dir.glob("*.py"))
            else:
                n_files = len({
                    c.get("file", "")
                    for c in (lm.get("components") or {}).values()
                    if c.get("file")
                })

            records.append({
                "run_id": run["run_id"],
                "model_id": model_id,
                "task_id": meta.get("task_id", task_id),
                "session_dir": sess_key,
                "modality": "agentic",
                "scenario_id": meta.get("primary_atomic_scenario", lm.get("primary_atomic_scenario", "")),
                "scenario_title": meta.get("task_family", ""),
                "sub_requirement_id": meta.get("variant", variant),
                "sub_requirement_description": f"c{meta.get('completion_index', completion_index)}",
                "detected_provider": lm.get("primary_provider", ""),
                "detected_ecosystem": lm.get("primary_ecosystem", ""),
                "detected_service": lm.get("dominant_ecosystem", ""),
                "detection_confidence": "high" if lm.get("completeness", 0) == 1.0 else "medium",
                "detection_method": "agentic_session",
                "completion_index": meta.get("completion_index", completion_index),
                "agentic_file_count": n_files,
            })
    except (json.JSONDecodeError, IOError):
        pass
    return records


# In-memory cache for per-model records, keyed by mtime of model dir
_RECORDS_CACHE = {}


def _dir_fingerprint(path):
    """Lightweight fingerprint: dir mtime + file count. Invalidates when content changes."""
    if not path.exists():
        return (0, 0)
    try:
        mtime = int(path.stat().st_mtime)
        count = sum(1 for _ in path.iterdir())
        return (mtime, count)
    except OSError:
        return (0, 0)


# ── Campaign runs as browsable results ──────────────────────
#
# The ablation campaigns under outputs/ablations/ keep their own layout: a cell
# per (scenario, model, condition, repetition), each holding a generated
# repository and per-file detector labels. That is the same information an
# agentic session carries, so campaign cells are surfaced as records in the
# same shape and the result browser can show them alongside the main runs. The
# extra dimension is the condition, which the record carries explicitly.

CAMPAIGN_MODALITY = "campaign"


_CAMPAIGN_INDEX = None

# Campaign runs sit at outputs/ablations/<group>/<name>/<run>/ or one level
# deeper for the nested extensions. Globbing those depths costs ~2ms; rglob
# walks every file under outputs/ablations/ (>130k) and cost 1.5s per call.
_CAMPAIGN_PLAN_GLOBS = ("*/*/*/plan.json", "*/*/*/*/plan.json")


def _campaign_run_index():
    """Every campaign run, keyed by a run_id the result browser can use."""
    global _CAMPAIGN_INDEX
    if _CAMPAIGN_INDEX is not None:
        return _CAMPAIGN_INDEX
    base = REPO_ROOT / "outputs" / "ablations"
    out = []
    if not base.is_dir():
        _CAMPAIGN_INDEX = out
        return out
    plans = sorted({q for pattern in _CAMPAIGN_PLAN_GLOBS for q in base.glob(pattern)})
    for plan in plans:
        run_root = plan.parent
        out.append({
            "run_id": "ablations/" + run_root.relative_to(base).as_posix(),
            "path": run_root,          # stands in for a labeled/ dir
            "run_root": run_root,
            "source": _repo_rel(run_root),
            "has_direct": False,
            "has_agentic": True,
            "campaign": True,
        })
    _CAMPAIGN_INDEX = out
    return out


def _shares(metrics, group):
    """Provider mass for one file group, as the campaign metrics record it."""
    node = ((metrics.get("groups") or {}).get("propagated") or {}).get(group) or {}
    return {
        "expected": node.get("expected"),
        "present": node.get("present"),
        "unknown": node.get("missing_or_unknown"),
        "providers": node.get("provider_share_all_expected") or {},
    }


_CAMPAIGN_CELLS = {}


def _campaign_cells(run_root):
    """Cells of a campaign run, each at its last attempt. Cached per run."""
    key_run = str(run_root)
    cached = _CAMPAIGN_CELLS.get(key_run)
    if cached is not None:
        return cached
    latest, counts = {}, {}
    root = run_root / "runs"
    if root.is_dir():
        # scenario/model/condition/rNNN/attempt_N — a bounded glob, not rglob.
        for attempt in sorted(root.glob("*/*/*/r*/attempt_*")):
            if not attempt.is_dir():
                continue
            parts = attempt.relative_to(root).parts
            if len(parts) != 5:
                continue
            key = parts[:4]
            counts[key] = counts.get(key, 0) + 1
            latest[key] = attempt
    cells = []
    for key, attempt in sorted(latest.items()):
        try:
            repetition = int(key[3][1:])
        except ValueError:
            continue
        cells.append({
            "scenario": key[0], "model": key[1], "condition": key[2],
            "repetition": repetition, "attempt": attempt,
            "attempts": counts[key],
        })
    _CAMPAIGN_CELLS[key_run] = cells
    return cells


def _campaign_task_id(scenario, condition):
    """A task id that reads as what the cell is: scenario under a condition."""
    return f"{CAMPAIGN_MODALITY}_{scenario}__{condition}"


def _build_campaign_records(run, model_id):
    """Campaign cells for one model, in the record shape the browser expects."""
    records = []
    for cell in _campaign_cells(run["run_root"]):
        if cell["model"] != model_id:
            continue
        attempt = cell["attempt"]
        try:
            metrics = _read_json(attempt / "metrics.json")
        except Exception:
            metrics = {}
        try:
            status = _read_json(attempt / "status.json")
        except Exception:
            status = {}
        downstream = _shares(metrics, "downstream")
        providers = downstream.get("providers") or {}
        dominant = max(providers, key=providers.get) if providers else ""
        labels = metrics.get("file_labels_explicit") or {}
        records.append({
            "run_id": run["run_id"],
            "model_id": model_id,
            "task_id": _campaign_task_id(cell["scenario"], cell["condition"]),
            "session_dir": f"{cell['scenario']}/{cell['model']}/{cell['condition']}/r{cell['repetition']:03d}",
            "modality": CAMPAIGN_MODALITY,
            "condition": cell["condition"],
            "scenario_id": cell["scenario"],
            "scenario_title": cell["condition"],
            "sub_requirement_id": cell["condition"],
            "sub_requirement_description": f"r{cell['repetition']}",
            "detected_provider": dominant,
            "detected_ecosystem": dominant,
            "detected_service": ", ".join(f"{k} {v:.0%}" for k, v in
                                          sorted(providers.items(), key=lambda kv: -kv[1])),
            "detection_confidence": "high" if status.get("state") == "completed" else "medium",
            "detection_method": "campaign_cell",
            "completion_index": cell["repetition"],
            "agentic_file_count": len(labels),
        })
    return records


def _seed_files(task):
    """Files supplied to the model as code, as {name: content}.

    Only the assigned-initial-provider campaign uses these, and it records them
    as [{"file": ..., "content": ...}] rather than bare names — comparing a
    filename against the raw list never matches.
    """
    out = {}
    for entry in task.get("seed_files") or []:
        if isinstance(entry, dict):
            name = entry.get("file") or entry.get("path") or entry.get("name")
            if name:
                out[name] = entry.get("content") or ""
        elif isinstance(entry, str):
            out[entry] = ""
    return out


def _campaign_prompt(attempt, task=None):
    """The prompt as the model received it, plus the system prompt.

    a1/a2/a3 send one prompt, recorded verbatim in prompt.txt and covered by
    the cell's prompt_sha256. a4 asks for one file per turn in a fresh
    conversation, so its prompt.txt holds the whole sequence as a JSON array
    and each turn is also written to steps/NN/prompt.txt. Rendering the array
    raw shows a JSON blob, so the turns are laid out in order instead.
    """
    parts = []
    system = attempt / "system_prompt.txt"
    if system.exists():
        parts.append("=== SYSTEM PROMPT ===\n"
                     + system.read_text(encoding="utf-8", errors="replace").strip())

    # An anchor file is handed to the model as existing code, so it is part of
    # the input even though it is not part of the prompt text.
    for name, content in _seed_files(task or {}).items():
        parts.append(f"=== SUPPLIED FILE (anchor): {name} ===\n{content.strip()}")

    prompt = attempt / "prompt.txt"
    raw = prompt.read_text(encoding="utf-8", errors="replace") if prompt.exists() else ""

    turns = None
    if raw.lstrip().startswith("["):
        try:
            loaded = json.loads(raw)
            if isinstance(loaded, list) and all(isinstance(x, str) for x in loaded):
                turns = loaded
        except json.JSONDecodeError:
            turns = None

    if turns is None:
        if raw.strip():
            parts.append("=== PROMPT ===\n" + raw.strip())
    else:
        # Prefer each step's own file: it is the text that turn actually sent.
        steps = sorted((attempt / "steps").glob("*/prompt.txt")) \
            if (attempt / "steps").is_dir() else []
        if len(steps) == len(turns):
            turns = [s.read_text(encoding="utf-8", errors="replace") for s in steps]
        for i, turn in enumerate(turns, start=1):
            parts.append(f"=== TURN {i} of {len(turns)} "
                         f"(fresh conversation) ===\n{turn.strip()}")

    return "\n\n".join(parts)


def _campaign_generation_order(attempt, task, roles):
    """The order the files were produced in, and how firmly that is known.

    The agent-driven campaigns (assigned / instructed initial provider) record
    every tool call in trace.json with a timestamp, so the sequence is observed.
    Staged disclosure keeps its own per-step event list. Single-shot generation
    emits everything in one response, so there is no recorded sequence at all —
    only the order the files appear in the text, which is reported as inferred
    so it is not mistaken for a measurement.
    """
    def entry(n, tool, name):
        return {"n": n, "tool": tool, "file": name,
                "role": roles.get(name, {}).get("role", ""),
                "ecosystem": roles.get(name, {}).get("ecosystem")}

    # 1. staged disclosure: its own event list
    audit = attempt / "disclosure_audit.json"
    if audit.exists():
        try:
            events = (_read_json(audit).get("generation_order") or {}).get("events") or []
        except Exception:
            events = []
        if events:
            ordered = sorted(events, key=lambda e: (e.get("step") or 0, e.get("start") or 0))
            return {
                "source": "disclosure_audit.json",
                "observed": True,
                "note": "one file per turn, each in a fresh conversation",
                "events": [dict(entry(i, e.get("tool") or "write", e.get("file") or ""),
                                step=e.get("step"))
                           for i, e in enumerate(ordered, start=1)],
            }

    # 2. agent runs: tool calls in the trace
    trace = attempt / "trace.json"
    if trace.exists():
        try:
            parts = _read_json(trace).get("parts") or []
        except Exception:
            parts = []
        calls = []
        for part in parts:
            data = part.get("data") if isinstance(part, dict) else None
            if not isinstance(data, dict) or "tool" not in data:
                continue
            state = data.get("state") or {}
            inputs = state.get("input") if isinstance(state, dict) else None
            path = (inputs or {}).get("filePath") or (inputs or {}).get("path") or ""
            started = ((state.get("time") or {}).get("start")
                       if isinstance(state, dict) else None)
            calls.append((started or 0, data.get("tool") or "", Path(path).name if path else ""))
        calls = [c for c in calls if c[2]]
        if calls:
            calls.sort(key=lambda c: c[0])
            return {
                "source": "trace.json",
                "observed": True,
                "note": "agent tool calls, in the order the runtime recorded them",
                "events": [entry(i, tool, name) for i, (_, tool, name) in
                           enumerate(calls, start=1)],
            }

    # 3. single response: position in the text, which is not a record of order
    response = attempt / "response.json"
    expected = list(roles)   # keyed by file name by the caller
    if response.exists() and expected:
        try:
            text = _read_json(response).get("output_text") or ""
        except Exception:
            text = ""
        seen, positions = set(), []
        for name in expected:
            at = text.find(name)
            if at >= 0 and name not in seen:
                seen.add(name)
                positions.append((at, name))
        if positions:
            positions.sort()
            return {
                "source": "response.json",
                "observed": False,
                "note": "generated in one response; this is the order the files "
                        "appear in the text, not a recorded sequence",
                "events": [entry(i, "emit", name) for i, (_, name) in
                           enumerate(positions, start=1)],
            }
    return None


def _campaign_detail(run, model_id, task_id, completion_index, session_dir):
    """One campaign cell, in the same shape as an agentic session detail."""
    for cell in _campaign_cells(run["run_root"]):
        if cell["model"] != model_id or cell["repetition"] != completion_index:
            continue
        if task_id and _campaign_task_id(cell["scenario"], cell["condition"]) != task_id:
            continue
        key = f"{cell['scenario']}/{cell['model']}/{cell['condition']}/r{cell['repetition']:03d}"
        if session_dir and session_dir != key:
            continue
        attempt = cell["attempt"]
        try:
            metrics = _read_json(attempt / "metrics.json")
        except Exception:
            metrics = {}
        labels = metrics.get("file_labels_explicit") or {}
        task = {}
        if (attempt / "input.json").exists():
            try:
                task = _read_json(attempt / "input.json").get("task") or {}
            except Exception:
                task = {}

        seeded = _seed_files(task)
        components = {}
        for name, label in sorted(labels.items()):
            ecosystems = label.get("detected_ecosystems") or []
            key = name[:-3] if name.endswith(".py") else name
            components[key] = {
                "file": name,
                "atomic_scenario": cell["scenario"],
                "provider": (label.get("detected_providers") or [None])[0],
                "ecosystem": ecosystems[0] if ecosystems else None,
                "service": label.get("detected_service") or label.get("service"),
                "confidence": label.get("confidence"),
                "detected_ecosystems": ecosystems,
                "role": ("anchor" if name in seeded
                         else "aligned core" if name in (task.get("aligned_core_files") or [])
                         else "context" if name in (task.get("aligned_context_files") or [])
                         else "downstream" if name in (task.get("downstream_files") or [])
                         else ""),
            }

        files = {}
        repo = attempt / "repository"
        for name in sorted(labels):
            path = repo / name
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if len(text) > MAX_OUTPUT_LEN:
                text = text[:MAX_OUTPUT_LEN] + "\n\n... [truncated]"
            files[name] = text

        prompt_text = _campaign_prompt(attempt, task)
        # Staged-disclosure cells carry ten turns plus a system prompt, so allow
        # more room before truncating than a single-prompt cell needs.
        limit = MAX_OUTPUT_LEN * 8
        if len(prompt_text) > limit:
            prompt_text = prompt_text[:limit] + "\n\n... [truncated]"

        return {
            "prompt_text": prompt_text,
            "output_text": "",
            "agentic_files": files,
            "agentic_components": components,
            "generation_order": _campaign_generation_order(
                attempt, task, {c["file"]: c for c in components.values()}),
            "agentic_metrics": {
                "condition": cell["condition"],
                "repetition": cell["repetition"],
                "attempts": cell["attempts"],
                "aligned_core_share": (_shares(metrics, "aligned_core") or {}).get("providers"),
                "downstream_share": (_shares(metrics, "downstream") or {}).get("providers"),
                "path": _repo_rel(attempt),
            },
        }
    return None


def _build_model_records(run, mid):
    """Build lightweight records for a single model. Cached."""
    if run.get("campaign"):
        return _build_campaign_records(run, mid)
    labeled = run["path"]
    # Cache key: run_id + model_id + dir fingerprints for all modalities
    fp = tuple(
        _dir_fingerprint(labeled / m / mid)
        for m in ("nli", "fim", "reference_open")
    )
    agentic_dir = labeled.parent / "raw" / "agentic" / mid
    fp += (_dir_fingerprint(agentic_dir),)
    key = (run["run_id"], mid, fp)
    if key in _RECORDS_CACHE:
        return _RECORDS_CACHE[key]

    records = []
    for modality in ["nli", "fim", "reference_open"]:
        model_dir = labeled / modality / mid
        if not model_dir.is_dir():
            continue
        for json_file in sorted(model_dir.glob("*.json")):
            try:
                with open(json_file) as f:
                    rec = json.load(f)
            except (json.JSONDecodeError, IOError):
                continue
            records.append({
                "run_id": run["run_id"],
                "model_id": mid,
                "task_id": rec.get("task_id", ""),
                "modality": rec.get("modality", modality),
                "scenario_id": rec.get("scenario_id", ""),
                "scenario_title": rec.get("scenario_title", ""),
                "sub_requirement_id": rec.get("sub_requirement_id", ""),
                "sub_requirement_description": rec.get("sub_requirement_description", ""),
                "detected_provider": rec.get("detected_provider", ""),
                "detected_ecosystem": rec.get("detected_ecosystem", ""),
                "detected_service": rec.get("detected_service", ""),
                "detection_confidence": rec.get("detection_confidence", ""),
                "detection_method": rec.get("detection_method", ""),
                "completion_index": rec.get("completion_index", 0),
            })
    records.extend(_build_agentic_index(run, mid))
    _RECORDS_CACHE[key] = records
    return records


def _build_all_records(model_ids, run_ids=None):
    """Build lightweight record list for given model IDs (uses per-model cache)."""
    index = _load_hf_results_index()
    if index:
        wanted_models = set(model_ids)
        wanted_runs = set(run_ids or [])
        return [
            rec
            for rec in index.get("records", [])
            if rec.get("model_id") in wanted_models
            and (not wanted_runs or rec.get("run_id") in wanted_runs)
        ]

    records = []
    for run in _filter_runs(run_ids):
        for mid in model_ids:
            records.extend(_build_model_records(run, mid))
    return records


@app.route("/api/results")
def api_results_search():
    """Server-side filtered + paginated result list.

    Query params:
      model     - model ID or "__all__" (required)
      run       - comma-separated run IDs
      modality  - filter by modality
      scenario  - filter by scenario_id
      filter    - "unknown", "low_conf", or "all" (default)
      offset    - pagination offset (default 0)
      limit     - page size (default 200)
    Returns: { results: [...], total: N, offset: N, limit: N }
    """
    model = request.args.get("model", "")
    run_ids = _parse_csv_arg("run")
    modality = request.args.get("modality", "")  # comma-separated
    scenario = request.args.get("scenario", "")  # comma-separated
    subtask = request.args.get("subtask", "")    # comma-separated subtask suffixes (a/b/c/d)
    filt = request.args.get("filter", "all")
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 200))

    if not model:
        return jsonify({"results": [], "total": 0, "offset": 0, "limit": limit})

    # Determine which models to scan (comma-separated or __all__)
    if model == "__all__":
        model_ids = _discover_models(run_ids)
    else:
        model_ids = [m.strip() for m in model.split(",") if m.strip()]

    records = _build_all_records(model_ids, run_ids)

    # Apply filters (support comma-separated multi-select)
    if modality:
        modalities = set(m.strip() for m in modality.split(","))
        records = [r for r in records if r["modality"] in modalities]
    if scenario:
        scenarios = set(s.strip() for s in scenario.split(","))
        records = [r for r in records if r["scenario_id"] in scenarios]
    if subtask:
        # Subtask suffixes are the last `_<letter>` of the direct task_id
        # (e.g. fim_S18_d -> "d"). Agentic tasks have no subtask suffix and
        # are excluded when this filter is active.
        suffixes = set(s.strip().lower() for s in subtask.split(",") if s.strip())
        records = [
            r for r in records
            if r.get("task_id", "").rsplit("_", 1)[-1].lower() in suffixes
        ]
    if filt == "unknown":
        records = [
            r
            for r in records
            if r["detection_confidence"] == "none"
            or r["detected_ecosystem"] == "unknown"
            or not r["detected_ecosystem"]
        ]
    elif filt == "low_conf":
        records = [
            r
            for r in records
            if r["detection_confidence"] in ("low", "medium")
        ]

    # Sort
    records.sort(
        key=lambda r: (
            r["run_id"],
            r["model_id"],
            r["modality"],
            r["scenario_id"],
            r.get("sub_requirement_id", ""),
            r["completion_index"],
        )
    )

    total = len(records)
    page = records[offset : offset + limit]

    return jsonify(
        {"results": page, "total": total, "offset": offset, "limit": limit}
    )


@app.route("/api/results/<model_id>")
def api_results_model(model_id):
    """Return lightweight result list for a single model."""
    records = _build_all_records([model_id], _parse_csv_arg("run"))
    records.sort(
        key=lambda r: (
            r["run_id"],
            r["modality"],
            r["scenario_id"],
            r.get("sub_requirement_id", ""),
            r["completion_index"],
        )
    )
    return jsonify(records)


# ── API: Single result detail (on-demand) ─────────────────────

@app.route("/api/result-detail/<model_id>/<task_id>/<int:completion_index>")
def api_result_detail(model_id, task_id, completion_index):
    """Return full detail for one result (prompt, output, agentic files)."""
    run_ids = _parse_csv_arg("run")
    wanted_modality = request.args.get("modality", "")
    wanted_session = request.args.get("session_dir", "")

    index = _load_hf_results_index()
    if index:
        wanted_runs = set(run_ids or [])
        runs_by_id = {run["run_id"]: run for run in _discover_runs()}
        for rec in index.get("records", []):
            if wanted_runs and rec.get("run_id") not in wanted_runs:
                continue
            if wanted_modality and rec.get("modality") != wanted_modality:
                continue
            if wanted_session and rec.get("session_dir", "") != wanted_session:
                continue
            if rec.get("model_id") != model_id:
                continue
            if rec.get("task_id") != task_id or rec.get("completion_index") != completion_index:
                continue

            if rec.get("modality") != "agentic":
                try:
                    full = json.loads(_hf_result_file_text(rec["source_file"]))
                except Exception as e:
                    return jsonify({"error": f"HF labeled result load failed: {e}"}), 502
                output_text = full.get("output_text", "")
                if output_text and len(output_text) > MAX_OUTPUT_LEN:
                    output_text = output_text[:MAX_OUTPUT_LEN] + "\n\n... [truncated]"
                return jsonify({
                    "prompt_text": full.get("prompt_text", ""),
                    "output_text": output_text,
                })

            run = runs_by_id.get(rec.get("run_id"))
            if not run:
                return jsonify({"error": "run not found"}), 404
            try:
                all_ag = json.loads(_hf_result_file_text(rec["source_file"]))
            except Exception as e:
                return jsonify({"error": f"HF agentic labels load failed: {e}"}), 502
            arec = None
            if isinstance(all_ag, list):
                for candidate in all_ag:
                    sess_key = (
                        f"{candidate.get('task_id')}__"
                        f"{candidate.get('variant', 'free')}__"
                        f"c{candidate.get('completion_index', 1)}"
                    )
                    if (
                        candidate.get("model_id") == model_id
                        and candidate.get("task_id") == task_id
                        and candidate.get("completion_index") == completion_index
                        and (not wanted_session or sess_key == wanted_session)
                    ):
                        arec = candidate
                        break
            if arec is None:
                return jsonify({"error": "agentic label not found"}), 404

            variant = arec.get("variant", "free")
            sess_key = f"{task_id}__{variant}__c{completion_index}"
            session_dir = run["run_root"] / "raw" / "agentic" / model_id / sess_key
            meta_text = _read_agentic_raw_file(
                run, session_dir, model_id, sess_key, "_meta.json"
            )
            try:
                meta = json.loads(meta_text) if meta_text else {}
            except json.JSONDecodeError:
                meta = {}
            prompt_text = meta.get("prompt_text", "")
            if prompt_text and len(prompt_text) > MAX_OUTPUT_LEN * 2:
                prompt_text = prompt_text[:MAX_OUTPUT_LEN * 2] + "\n\n... [truncated]"

            files = {}
            file_names = sorted({
                c.get("file", "")
                for c in (arec.get("components") or {}).values()
                if c.get("file")
            })
            for file_name in file_names:
                content = _read_agentic_raw_file(
                    run, session_dir, model_id, sess_key, file_name
                )
                if not content:
                    continue
                if len(content) > MAX_OUTPUT_LEN:
                    content = content[:MAX_OUTPUT_LEN] + "\n\n... [truncated]"
                files[file_name] = content

            agentic_metrics = {
                mk: arec.get(mk)
                for mk in [
                    "dominant_ecosystem", "ecosystem_coherence",
                    "primary_ecosystem", "primary_provider",
                    "scored_affil_rate", "completeness",
                    "aligned_core_ecosystem_coherence",
                    "downstream_ecosystem_coherence",
                    "variant",
                ]
                if arec.get(mk) is not None
            }
            return jsonify({
                "prompt_text": prompt_text,
                "output_text": "",
                "agentic_files": files,
                "agentic_components": arec.get("components", {}),
                "agentic_metrics": agentic_metrics,
            })

    for run in _filter_runs(run_ids):
        if run.get("campaign"):
            if wanted_modality and wanted_modality != CAMPAIGN_MODALITY:
                continue
            detail = _campaign_detail(run, model_id, task_id,
                                      completion_index, wanted_session)
            if detail is not None:
                return jsonify(detail)
            continue

        labeled = run["path"]

        # Try direct modalities
        for modality in ["nli", "fim", "reference_open"]:
            if wanted_modality and wanted_modality != modality:
                continue
            model_dir = labeled / modality / model_id
            if not model_dir.is_dir():
                continue
            for json_file in model_dir.glob("*.json"):
                try:
                    with open(json_file) as f:
                        rec = json.load(f)
                except (json.JSONDecodeError, IOError):
                    continue
                if rec.get("task_id") == task_id and rec.get("completion_index") == completion_index:
                    output_text = rec.get("output_text", "")
                    if output_text and len(output_text) > MAX_OUTPUT_LEN:
                        output_text = output_text[:MAX_OUTPUT_LEN] + "\n\n... [truncated]"
                    return jsonify({
                        "prompt_text": rec.get("prompt_text", ""),
                        "output_text": output_text,
                    })

        # Try agentic sessions
        if wanted_modality and wanted_modality != "agentic":
            continue
        agentic_raw_dir = labeled.parent / "raw" / "agentic" / model_id
        agentic_results = labeled / "agentic" / "results.json"
        if not agentic_results.exists():
            continue

        try:
            with open(agentic_results) as f:
                all_ag = json.load(f)
        except (json.JSONDecodeError, IOError):
            continue
        if not isinstance(all_ag, list):
            continue

        for arec in all_ag:
            if arec.get("model_id") != model_id:
                continue
            variant = arec.get("variant", "free")
            sess_key = f"{arec.get('task_id')}__{variant}__c{arec.get('completion_index', 1)}"
            if wanted_session and sess_key != wanted_session:
                continue
            if arec.get("task_id") != task_id or arec.get("completion_index") != completion_index:
                continue

            session_dir = agentic_raw_dir / sess_key
            meta_text = _read_agentic_raw_file(
                run, session_dir, model_id, sess_key, "_meta.json"
            )
            try:
                meta = json.loads(meta_text) if meta_text else {}
            except json.JSONDecodeError:
                meta = {}

            prompt_text = meta.get("prompt_text", "")
            if prompt_text and len(prompt_text) > MAX_OUTPUT_LEN * 2:
                prompt_text = prompt_text[:MAX_OUTPUT_LEN * 2] + "\n\n... [truncated]"

            files = {}
            if session_dir.is_dir():
                file_names = sorted(p.name for p in session_dir.glob("*.py"))
            else:
                file_names = sorted({
                    c.get("file", "")
                    for c in (arec.get("components") or {}).values()
                    if c.get("file")
                })
            for file_name in file_names:
                content = _read_agentic_raw_file(
                    run, session_dir, model_id, sess_key, file_name
                )
                if not content:
                    continue
                if len(content) > MAX_OUTPUT_LEN:
                    content = content[:MAX_OUTPUT_LEN] + "\n\n... [truncated]"
                files[file_name] = content

            agentic_components = arec.get("components", {})
            agentic_metrics = {
                mk: arec.get(mk)
                for mk in [
                    "dominant_ecosystem", "ecosystem_coherence",
                    "primary_ecosystem", "primary_provider",
                    "scored_affil_rate", "completeness",
                    "aligned_core_ecosystem_coherence",
                    "downstream_ecosystem_coherence",
                    "variant",
                ]
                if arec.get(mk) is not None
            }

            return jsonify({
                "prompt_text": prompt_text,
                "output_text": "",
                "agentic_files": files,
                "agentic_components": agentic_components,
                "agentic_metrics": agentic_metrics,
            })

    return jsonify({"error": "not found"}), 404


# ── API: Evaluations (persistent, server-side) ───────────────

def _load_evaluations():
    if EVAL_FILE.exists():
        try:
            with open(EVAL_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def _save_evaluations(evals):
    with open(EVAL_FILE, "w") as f:
        json.dump(evals, f, indent=2)


# ── Ablations ────────────────────────────────────────────────

# The ten ablations, each keyed by its directory under outputs/tables/. Four ran
# their own generation campaigns (outputs/ablations/), the option-order and
# runtime checks reuse the main pipeline with a different config
# (outputs/runs/.../variants/), and the rest are re-analyses of the main run.
ABLATION_CATALOG = [
    {"key": "option_order", "kind": "config variant",
     "runs_glob": "*/variants/option_order/**"},
    {"key": "agent_runtime", "kind": "config variant",
     "runs": ["agentic/complete/agents_sdk_full_5c",
              "agentic/complete/opencode_full_5c"]},
    {"key": "assigned_as_code", "kind": "campaign",
     "campaign": "initial_provider/assigned_as_code"},
    {"key": "by_instruction", "kind": "campaign",
     "campaign": "initial_provider/by_instruction"},
    {"key": "single_shot_multifile", "kind": "campaign",
     "campaign": "agentic_mechanism/single_shot_multifile"},
    {"key": "task_disclosure", "kind": "campaign",
     "campaign": "agentic_mechanism/task_disclosure"},
    {"key": "prompt_format", "kind": "re-analysis"},
    {"key": "concentration_vs_affiliation", "kind": "re-analysis"},
    {"key": "control_composition", "kind": "re-analysis"},
    {"key": "affiliation_definition", "kind": "re-analysis"},
]

_CONCERN = re.compile(r"\*\*Concern\.\*\*\s*(.+?)(?:\n\n|\Z)", re.S)


def _h1(text):
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


# "Provider-option order (paper Tables 10-11)" -> title + paper reference.
_PAPER_REF = re.compile(r"\s*\((paper [^)]+)\)\s*$", re.I)
# Campaign README titles are numbered internally: "Ablation 1: assigned ...".
_ABLATION_NO = re.compile(r"^Ablation\s+\d+\s*:\s*", re.I)
# Derived-table titles end with the kind of table they are.
_TABLE_SUFFIX = re.compile(r"\s*—\s*(results|headline)\s*$", re.I)


def _ablation_title(table_dir, code_rel=None):
    """A readable title, plus the paper reference if the docs name one.

    The derived tables carry the human title ("Assigned initial provider —
    results"); the campaign READMEs carry an internal number ("Ablation 1:
    assigned initial provider"). Prefer the former and strip the latter.
    """
    paper_ref = ""
    readme = table_dir / "README.md"
    if readme.exists():
        m = _PAPER_REF.search(_h1(readme.read_text(encoding="utf-8")))
        if m:
            paper_ref = m.group(1)
    for name in ("summary.md", "headline.md", "README.md"):
        candidate = table_dir / name
        if not candidate.exists():
            continue
        title = _h1(candidate.read_text(encoding="utf-8"))
        if not title:
            continue
        m = _PAPER_REF.search(title)
        if m:
            paper_ref = m.group(1)
            title = _PAPER_REF.sub("", title)
        title = _TABLE_SUFFIX.sub("", title).strip()
        if title:
            return title, paper_ref

    if code_rel:
        readme = PROJECT_ROOT / "ablations" / code_rel / "README.md"
        if readme.exists():
            title = _ABLATION_NO.sub("", _h1(readme.read_text(encoding="utf-8")))
            if title:
                return title[0].upper() + title[1:], paper_ref
    return "", paper_ref


def _ablation_concern(table_dir, code_rel=None):
    readme = table_dir / "README.md"
    if not readme.exists() and code_rel:
        readme = PROJECT_ROOT / "ablations" / code_rel / "README.md"
    if not readme.exists():
        return ""
    text = readme.read_text(encoding="utf-8")
    m = _CONCERN.search(text)
    if m:
        return " ".join(m.group(1).split())
    # Campaign READMEs open with a "Tests whether ..." paragraph instead.
    for para in text.split("\n\n")[1:]:
        para = para.strip()
        if para and not para.startswith(("#", "```", "|", "-", "*")):
            return " ".join(para.split())
    return ""


def _grid(cells, field):
    """Distinct values of one plan field, in first-seen order."""
    seen = []
    for cell in cells:
        value = cell.get(field)
        if value is not None and value not in seen:
            seen.append(value)
    return seen


_CELL_CACHE = {}


def _cells_on_disk(run):
    """The (scenario, model, condition, repetition) cells materialised in runs/.

    This is what the directory actually holds, which is the only thing that
    says whether an ablation's data is complete. progress.json describes one
    execution pass instead: a run that timed out on some cells and was finished
    by a later pass still reports itself as interrupted forever.
    """
    key = str(run)
    cached = _CELL_CACHE.get(key)
    if cached is not None:
        return cached
    found = set()
    root = run / "runs"
    if root.is_dir():
        for attempt in root.glob("*/*/*/r*/attempt_*"):
            parts = attempt.relative_to(root).parts
            if len(parts) >= 5:
                try:
                    found.add((parts[0], parts[1], parts[2], int(parts[3][1:])))
                except ValueError:
                    continue
    _CELL_CACHE[key] = found
    return found


def _planned_cells(plan):
    out = set()
    for cell in plan.get("cells") or []:
        try:
            out.add((cell["scenario"], cell["model"],
                     cell["condition"], cell["repetition"]))
        except KeyError:
            continue
    return out


def _campaign_runs(rel):
    """The generation passes of one ablation campaign, measured from disk."""
    base = REPO_ROOT / "outputs" / "ablations" / rel
    out = []
    plans = sorted({q for pattern in ("*/plan.json", "*/*/plan.json")
                    for q in base.glob(pattern)})
    for plan_path in plans:
        run = plan_path.parent
        try:
            plan = _read_json(plan_path)
        except Exception:
            continue
        cells = plan.get("cells") or []
        planned = _planned_cells(plan)
        present = _cells_on_disk(run)
        out.append({
            "run_id": run.relative_to(base.parent.parent).as_posix(),
            "name": run.name,
            "path": _repo_rel(run),
            "planned": len(planned),
            "on_disk": len(present),
            "models": _grid(cells, "model"),
            "conditions": _grid(cells, "condition"),
            "scenarios": len(_grid(cells, "scenario")),
            "timeout": plan.get("timeout"),
            "retained": len(plan.get("retained_attempts") or []),
            "_planned": planned,
            "_present": present,
        })

    # A pass whose plan is exactly what an earlier pass left unfinished is a
    # continuation of it, not a competing run. Decide every role first, then
    # assign: writing roles inside the scan overwrote ones already decided.
    continuation = set()
    for run in out:
        unfinished = run["_planned"] - run["_present"]
        if not unfinished:
            continue
        for other in out:
            if other is not run and other["_planned"] == unfinished:
                continuation.add(id(other))
    for run in out:
        if id(run) in continuation:
            run["role"] = "completion pass"
        elif len(out) == 1:
            run["role"] = "single pass"
        else:
            run["role"] = "generation pass"
    return out


def _campaign_coverage(runs):
    """Whether the passes together hold every cell the campaign planned.

    Cells on disk can outnumber planned cells: a completion pass materialises
    its predecessor's retained attempts, which belong to that earlier plan. So
    completeness is "every expected cell is present", not a raw count compare.
    """
    expected, present = set(), set()
    for run in runs:
        expected |= run["_planned"]
        present |= run["_present"]
    missing = expected - present
    return {
        "expected": len(expected),
        "covered": len(expected & present),
        "missing": len(missing),
        "extra": len(present - expected),
        "complete": not missing,
    }


def _variant_runs(run_ids):
    """Config-variant runs, which live under outputs/runs/ like the main study."""
    runs_root = REPO_ROOT / "outputs" / "runs"
    out = []
    for run_id in run_ids:
        run = runs_root / run_id
        if not run.is_dir():
            continue
        agentic = (run / "labeled" / "agentic").is_dir()
        models = []
        if agentic:
            try:
                rows = _read_json(run / "labeled" / "agentic" / "results.json")
                models = sorted({r.get("model_id") for r in rows if r.get("model_id")})
            except Exception:
                rows = []
        else:
            for modality_dir in sorted((run / "labeled").glob("*")):
                if modality_dir.is_dir():
                    models += [d.name for d in sorted(modality_dir.iterdir()) if d.is_dir()]
            models = sorted(set(models))
        out.append({
            "run_id": run_id,
            "name": run.name,
            "path": f"outputs/runs/{run_id}",
            "records": _count_labeled(run),
            "models": models,
            "kind": "agentic" if agentic else "direct",
        })
    return out


def _ablation_results(table_dir):
    """The ablation's own result write-up, inline, so it needs no extra click."""
    for name in ("summary.md", "headline.md"):
        path = table_dir / name
        if path.exists():
            return {"name": name, "path": _repo_rel(path),
                    "markdown": path.read_text(encoding="utf-8")}
    return None


@app.route("/api/ablations")
def api_ablations():
    """Every ablation: what it tests, the runs behind it, and its results."""
    tables_root = REPO_ROOT / "outputs" / "tables"
    runs_root = REPO_ROOT / "outputs" / "runs"
    known = {r["run_id"] for r in _discover_runs()}
    items = []

    for entry in ABLATION_CATALOG:
        table_dir = tables_root / entry["key"]
        title, paper_ref = _ablation_title(table_dir, entry.get("campaign"))
        tables = []
        if table_dir.is_dir():
            tables = sorted(
                ({"name": f.name, "path": _repo_rel(f), "bytes": f.stat().st_size}
                 for f in table_dir.glob("*")
                 if f.is_file() and f.name != "README.md"),
                key=lambda d: d["name"])

        coverage = None
        if entry.get("runs_glob"):
            runs = _variant_runs(sorted(r for r in known
                                        if "variants/option_order" in r))
        elif entry.get("runs"):
            runs = _variant_runs([r for r in entry["runs"] if r in known])
        elif entry.get("campaign"):
            runs = _campaign_runs(entry["campaign"])
            coverage = _campaign_coverage(runs)
            for run in runs:          # drop the private cell sets before serialising
                run.pop("_planned", None)
                run.pop("_present", None)
        else:
            runs = []

        items.append({
            "key": entry["key"],
            "kind": entry["kind"],
            "title": title or entry["key"].replace("_", " "),
            "paper_ref": paper_ref,
            "concern": _ablation_concern(table_dir, entry.get("campaign")),
            "tables": tables,
            "runs": runs,
            "results": _ablation_results(table_dir),
            "coverage": coverage,
            "run_root": ("outputs/runs" if entry["kind"] == "config variant"
                         else f"outputs/ablations/{entry.get('campaign', '')}"
                         if entry.get("campaign") else ""),
        })

    return jsonify({"ablations": items,
                    "tables_root": _repo_rel(tables_root),
                    "runs_root": _repo_rel(runs_root)})


@app.route("/api/ablations/table")
def api_ablation_table():
    """One derived table file, as text."""
    rel = request.args.get("path", "")
    safe = Path(rel)
    if not rel or safe.is_absolute() or ".." in safe.parts:
        return jsonify({"error": "bad path"}), 400
    target = REPO_ROOT / safe
    try:
        target.relative_to(REPO_ROOT / "outputs" / "tables")
    except ValueError:
        return jsonify({"error": "outside outputs/tables"}), 400
    if not target.is_file():
        return jsonify({"error": "not found"}), 404
    return jsonify({"path": rel, "name": target.name,
                    "text": target.read_text(encoding="utf-8", errors="replace")})


@app.route("/api/evaluations", methods=["GET"])
def get_evaluations():
    return jsonify(_load_evaluations())


@app.route("/api/evaluations", methods=["POST"])
def save_evaluation():
    """Save a single evaluation. Body: { key, evaluation }."""
    body = request.get_json()
    if not body or "key" not in body or "evaluation" not in body:
        return jsonify({"error": "need key and evaluation"}), 400

    evals = _load_evaluations()
    ev = body["evaluation"]
    key = body["key"]

    if ev.get("correct"):
        evals[key] = ev
    else:
        evals.pop(key, None)

    _save_evaluations(evals)
    return jsonify({"status": "saved", "total": len(evals)})


@app.route("/api/evaluations/bulk", methods=["POST"])
def bulk_upload_evaluations():
    """Bulk import evaluations. Body: array of evaluation objects."""
    arr = request.get_json()
    if not isinstance(arr, list):
        return jsonify({"error": "expected array"}), 400

    evals = _load_evaluations()
    imported = 0
    for ev in arr:
        if ev.get("model_id") and ev.get("task_id") and ev.get("correct"):
            key = "__".join([
                ev.get("run_id", ""),
                ev.get("model_id", ""),
                ev.get("modality", ""),
                ev.get("task_id", ""),
                ev.get("sub_requirement_id", ""),
                ev.get("session_dir", ""),
                f"c{ev.get('completion_index', 0)}",
            ])
            evals[key] = ev
            imported += 1

    _save_evaluations(evals)
    return jsonify({"status": "imported", "count": imported, "total": len(evals)})


# ── Main ─────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VIBench Explorer server")
    parser.add_argument("port", nargs="?", type=int, default=0,
                        help="Port number (default: auto-select a free port)")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--benchmark-source", default="auto",
                        choices=["auto", "hf", "local"],
                        help="Benchmark data source (default: auto)")
    parser.add_argument("--results-source", default="auto",
                        choices=["auto", "hf", "local"],
                        help="Result data source (default: auto)")
    parser.add_argument("--hf-benchmark-repo", default=HF_BENCHMARK_REPO,
                        help="Hugging Face benchmark dataset repo")
    parser.add_argument("--hf-results-repo", default=HF_RESULTS_REPO,
                        help="Hugging Face results dataset repo")
    args = parser.parse_args()
    BENCHMARK_SOURCE = args.benchmark_source
    RESULTS_SOURCE = args.results_source
    HF_BENCHMARK_REPO = args.hf_benchmark_repo
    HF_RESULTS_REPO = args.hf_results_repo

    if args.port == 0:
        # Find a free port
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            args.port = s.getsockname()[1]

    print(f"VIBench Explorer: http://{args.host}:{args.port}")
    print(f"  Code root:    {PROJECT_ROOT}")
    print(f"  Repo root:    {REPO_ROOT}")
    print(f"  Results source: {RESULTS_SOURCE}")
    print(f"  Search roots: {', '.join(str(p) for p in _result_search_dirs())}")
    print(f"  Models found: {len(_discover_models())}")
    app.run(host=args.host, port=args.port, debug=args.debug)
