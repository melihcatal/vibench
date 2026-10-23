#!/usr/bin/env python3
"""Package a run's control-model outputs as a versioned baseline bundle.

A baseline bundle lets anyone evaluate a single new model against the
published control runs without re-running the controls themselves:

    python scripts/evaluation/baselines/build_control_baseline.py \
        --run direct/complete/full_5c --id controls-2026q2

    python scripts/evaluation/core/evaluate.py \
        --run direct/complete/my_new_model_run --baseline controls-2026q2

The bundle is a run-shaped directory (so the standard labeled-output
loader reads it unchanged) under outputs/baselines/<id>/:

    labeled/<modality>/<control_model_id>/*.json   copied from the source run
    manifest.json                                  provenance + record counts

Only models with role "control" in the registry are packaged. Pass
--agentic-run to also package the agentic control rows
(labeled/agentic/results.json) from the paired agentic run.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import sys as _sys
from pathlib import Path as _Path
# The evaluation modules form one namespace, grouped into folders for
# readability only, so every group is importable from every other.
_EVAL_DIR = _Path(__file__).resolve().parents[1]
for _group in ("core", "gini", "tables", "baselines", "audit"):
    _sys.path.insert(0, str(_EVAL_DIR / _group))
import evaluate as direct_eval  # noqa: E402
import model_registry as registry  # noqa: E402

BASE_DIR = Path(__file__).resolve().parents[3]
REPO_DIR = BASE_DIR.parent
BASELINES_DIR = REPO_DIR / "outputs" / "control_sets"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--run", required=True, help="Source direct run ID or directory containing the control outputs")
    parser.add_argument("--agentic-run", default=None,
                        help="Optional agentic run ID/directory; its labeled control rows are packaged too")
    parser.add_argument("--id", required=True, help="Baseline ID, e.g. controls-2026q2")
    parser.add_argument("--output-root", type=Path, default=BASELINES_DIR,
                        help="Directory to create the bundle in (default: outputs/baselines)")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing bundle with the same ID")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = direct_eval.resolve_run_dir(args.run)
    if not run_dir:
        raise SystemExit(f"Run '{args.run}' not found")
    labeled_dir = run_dir / "labeled"
    if not labeled_dir.is_dir():
        raise SystemExit(f"{run_dir} has no labeled/ directory")

    controls = registry.strict_controls()
    out_dir = args.output_root / args.id
    if out_dir.exists():
        if not args.force:
            raise SystemExit(f"{out_dir} already exists (use --force to rebuild)")
        shutil.rmtree(out_dir)

    counts: dict[str, int] = {model_id: 0 for model_id in controls}
    for modality_dir in sorted(labeled_dir.iterdir()):
        if not modality_dir.is_dir() or modality_dir.name not in direct_eval.DIRECT_MODALITIES:
            continue
        for model_id in controls:
            src = modality_dir / model_id
            if not src.is_dir():
                continue
            dst = out_dir / "labeled" / modality_dir.name / model_id
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src, dst)
            counts[model_id] += sum(1 for _ in dst.glob("*.json"))

    missing = [m for m, n in counts.items() if n == 0]
    if missing:
        raise SystemExit(f"No labeled outputs found for control models {missing} in {run_dir}")

    agentic_counts: dict[str, int] = {}
    agentic_source = None
    if args.agentic_run:
        agentic_run_dir = direct_eval.resolve_run_dir(args.agentic_run)
        if not agentic_run_dir:
            raise SystemExit(f"Agentic run '{args.agentic_run}' not found")
        results_path = agentic_run_dir / "labeled" / "agentic" / "results.json"
        if not results_path.exists():
            raise SystemExit(f"{agentic_run_dir} has no labeled/agentic/results.json")
        with open(results_path) as f:
            rows = json.load(f)
        control_rows = [r for r in rows if r.get("model_id") in set(controls)]
        if not control_rows:
            raise SystemExit(f"No control-model rows in {results_path}")
        out_path = out_dir / "labeled" / "agentic" / "results.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(control_rows, indent=2) + "\n")
        for r in control_rows:
            agentic_counts[r["model_id"]] = agentic_counts.get(r["model_id"], 0) + 1
        agentic_source = (str(agentic_run_dir.relative_to(REPO_DIR))
                          if agentic_run_dir.is_relative_to(REPO_DIR) else str(agentic_run_dir))

    manifest = {
        "baseline_id": args.id,
        "setting": "direct+agentic" if agentic_counts else "direct",
        "source_run": str(run_dir.relative_to(REPO_DIR)) if run_dir.is_relative_to(REPO_DIR) else str(run_dir),
        "control_models": controls,
        "records_per_model": counts,
        "total_records": sum(counts.values()),
        "agentic_source_run": agentic_source,
        "agentic_rows_per_model": agentic_counts or None,
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "note": "Control-model labeled outputs packaged for --baseline evaluation. "
                "VIB scores computed against this bundle must cite the baseline_id.",
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Baseline '{args.id}': {manifest['total_records']} direct records "
          f"({', '.join(f'{m}={n}' for m, n in counts.items())})")
    if agentic_counts:
        print(f"  + {sum(agentic_counts.values())} agentic rows "
              f"({', '.join(f'{m}={n}' for m, n in agentic_counts.items())})")
    print(out_dir)


if __name__ == "__main__":
    main()
