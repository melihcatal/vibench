#!/usr/bin/env python3
"""Derive each ablation's paper-facing numbers from the analysis snapshots.

Reads the snapshots under ablations/snapshots/ and writes, for every ablation,

    outputs/tables/<ablation>/summary.json   machine-readable
    outputs/tables/<ablation>/summary.md     the table used in the paper

Every value is read out of a snapshot; nothing is hardcoded here. Re-run with

    python ablations/snapshots/make_summaries.py

Snapshot provenance (recorded in each summary.json as `source`):

    ablation 1, 3  a1_a3_retry_snapshot_20260921_finished/bootstrap_results.json
    ablation 2     20260919_full_a2_a3/results.json
    ablation 4     20260920_a4_20s_finished_snapshot/results.json
"""

from __future__ import annotations

import json
from pathlib import Path

SNAPSHOTS = Path(__file__).resolve().parent
TABLES = SNAPSHOTS.parents[2] / "outputs" / "tables"

# The snapshots were written while the campaigns were numbered, and are kept
# byte-for-byte as recorded (each carries its own script_sha256). This maps the
# directory names used in this package to the keys inside those snapshots.
SNAPSHOT_KEYS = {
    "assigned_as_code": "1",
    "single_shot_multifile": "ablation_2",
    "by_instruction": "3",
    "task_disclosure": "4",
}

A1_A3_SNAPSHOT = "a1_a3_retry_snapshot_20260921_finished/bootstrap_results.json"
A2_SNAPSHOT = "20260919_full_a2_a3/results.json"
A4_SNAPSHOT = "20260920_a4_20s_finished_snapshot/results.json"

# Share of task-aligned core files assigned to the affiliated ecosystem.
# `core` is computed over runs with extractable output (the headline figure);
# `all_assigned_core_missing_zero` keeps every run and scores an unextractable
# one as zero, giving a conservative lower bound. Both are reported.
A2_METRIC = "core"
A2_METRIC_CONSERVATIVE = "all_assigned_core_missing_zero"


def load(rel: str):
    return json.loads((SNAPSHOTS / rel).read_text())


def pct(value: float) -> float:
    """Snapshot shares are stored as proportions; report percentages."""
    return round(value * 100, 1)


def anchor_rows(section: dict, key: str) -> dict:
    agg = section[key]["aggregate"]
    return {
        "scenarios": len(section[key]["scenarios"]),
        "all_anchors_pct": round(agg["all_anchor"]["mean"], 1),
        "all_anchors_ci95": [round(v, 1) for v in agg["all_anchor"]["ci95"]],
        "own_ecosystem_anchor_pct": round(agg["own_anchor"]["mean"], 1),
        "competing_anchor_pct": round(agg["competing_anchor"]["mean"], 1),
        "own_minus_competing_pp": round(agg["difference"]["mean"], 1),
        "own_minus_competing_ci95": [round(v, 1) for v in agg["difference"]["ci95"]],
    }


def build_anchor_summary(which: str) -> dict:
    """Ablations 1 and 3: anchor-following retention and the affiliation gap.

    Both attempt scopes are reported. `latest_finished` counts each run at its
    last finished attempt (after timeout retries) and is the scope reported in
    the paper; `first_finished` counts first attempts only.
    """
    raw = load(A1_A3_SNAPSHOT)
    out = {
        "source": A1_A3_SNAPSHOT,
        "method": raw["method"],
        "replicates": raw["replicates"],
        "seed": raw["seed"],
        "reported_scope": "latest_finished",
        "scopes": {},
    }
    for scope, results in raw["results"].items():
        out["scopes"][scope] = {
            "downstream_files": anchor_rows(results["downstream"], which),
            "generated_core_files": anchor_rows(results["generated_core"], which),
        }
    return out


def build_a2_summary() -> dict:
    """Ablation 2: affiliated share in task-aligned core files, by condition."""
    raw = load(A2_SNAPSHOT)
    per_model = {}
    for model, body in raw[SNAPSHOT_KEYS["single_shot_multifile"]].items():
        row = {}
        for condition, stats in body["conditions"].items():
            metric = stats[A2_METRIC]
            conservative = stats[A2_METRIC_CONSERVATIVE]
            row[condition] = {
                "affiliated_core_share_pct": pct(metric["mean"]),
                "ci95": [pct(v) for v in metric["ci"]],
                "extractable_runs": metric["n"],
                "scenarios": metric["scenarios"],
                "all_runs_unextractable_as_zero_pct": pct(conservative["mean"]),
                "all_runs_unextractable_as_zero_ci95": [pct(v) for v in conservative["ci"]],
                "all_runs": conservative["n"],
            }
        per_model[model] = row
    return {
        "source": A2_SNAPSHOT,
        "metric": A2_METRIC,
        "metric_conservative": A2_METRIC_CONSERVATIVE,
        "created": raw.get("created"),
        "models": per_model,
    }


def build_a4_summary() -> dict:
    """Ablation 4: persistence conditional on an affiliated first file.

    Both attempt scopes are reported. `first_attempt` is the scope reported in
    the paper; `latest_finished_attempt` counts each run at its last finished
    attempt, after timeout retries.
    """
    raw = load(A4_SNAPSHOT)
    out = {
        "source": A4_SNAPSHOT,
        "note": raw.get("note"),
        "reported_scope": "first_attempt",
        "scopes": {},
    }
    for scope, summaries in raw["summaries"].items():
        per_model = {}
        for model, body in summaries.items():
            row = {}
            for condition, stats in body["conditions"].items():
                conditional = stats["conditional"]
                row[condition] = {
                    "conditional_persistence_pct": pct(conditional["mean"]),
                    "ci95": [pct(v) for v in conditional["ci"]],
                    "runs": conditional["n"],
                    "scenarios": conditional["scenarios"],
                    "protocol_verified": stats.get("conditional_protocol_verified"),
                }
            per_model[model] = row
        out["scopes"][scope] = per_model
    return out


def md_anchor(title: str, summary: dict) -> str:
    reported = summary["reported_scope"]
    lines = [f"# {title} — results", "",
             f"Derived from `ablations/snapshots/{summary['source']}` by "
             "`ablations/snapshots/make_summaries.py`.", "",
             f"{summary['method']} {summary['replicates']} replicates, seed {summary['seed']}.", ""]
    for scope in sorted(summary["scopes"], key=lambda s: s != reported):
        tag = " (reported in the paper)" if scope == reported else ""
        lines += [f"## Attempt scope: `{scope}`{tag}", "",
                  "| File set | Anchor followed (all anchors) | Own-ecosystem anchor | Competing anchor | Own − competing |",
                  "| --- | --- | --- | --- | --- |"]
        for label, key in (("Downstream files", "downstream_files"),
                           ("Generated core files", "generated_core_files")):
            r = summary["scopes"][scope][key]
            lines.append(
                f"| {label} | {r['all_anchors_pct']}% "
                f"[{r['all_anchors_ci95'][0]}, {r['all_anchors_ci95'][1]}] | "
                f"{r['own_ecosystem_anchor_pct']}% | {r['competing_anchor_pct']}% | "
                f"+{r['own_minus_competing_pp']} pp "
                f"[{r['own_minus_competing_ci95'][0]}, {r['own_minus_competing_ci95'][1]}] |")
        lines.append("")
    lines += ["Percentile 95% CIs from a paired scenario-cluster bootstrap. "
              "Values are scenario-balanced over all 20 scenarios. `latest_finished` "
              "counts each run at its last finished attempt, after timeout retries; "
              "`first_finished` counts first attempts only.", ""]
    return "\n".join(lines)


def md_a2(summary: dict) -> str:
    lines = ["# Single-shot multi-file generation — results", "",
             f"Derived from `ablations/snapshots/{summary['source']}` by "
             "`ablations/snapshots/make_summaries.py`.", "",
             "Share of task-aligned core files assigned to the model's affiliated "
             f"ecosystem (`{summary['metric']}`), over runs with extractable output.", "",
             "| Model | Single-shot | Original agentic | Difference |",
             "| --- | --- | --- | --- |"]
    for model, row in summary["models"].items():
        single = row.get("single_shot")
        agentic = row.get("original_agentic")
        if not (single and agentic):
            continue
        delta = round(agentic["affiliated_core_share_pct"] - single["affiliated_core_share_pct"], 1)
        lines.append(
            f"| `{model}` | {single['affiliated_core_share_pct']}% "
            f"[{single['ci95'][0]}, {single['ci95'][1]}] | "
            f"{agentic['affiliated_core_share_pct']}% "
            f"[{agentic['ci95'][0]}, {agentic['ci95'][1]}] | "
            f"{'+' if delta > 0 else ''}{delta} pp |")
    lines += ["", "Difference is original agentic minus single-shot: a positive value means the "
                  "affiliated share was higher with agent tools than in one response.", "",
              "Conservative bound, keeping every run and scoring an unextractable one as "
              f"zero (`{summary['metric_conservative']}`):", "",
              "| Model | Single-shot | Original agentic |", "| --- | --- | --- |"]
    for model, row in summary["models"].items():
        single = row.get("single_shot")
        agentic = row.get("original_agentic")
        if not (single and agentic):
            continue
        lines.append(
            f"| `{model}` | {single['all_runs_unextractable_as_zero_pct']}% "
            f"({single['extractable_runs']}/{single['all_runs']} runs extractable) | "
            f"{agentic['all_runs_unextractable_as_zero_pct']}% "
            f"({agentic['extractable_runs']}/{agentic['all_runs']}) |")
    lines.append("")
    return "\n".join(lines)


def md_a4(summary: dict) -> str:
    lines = ["# Full versus staged task disclosure — results", "",
             f"Derived from `ablations/snapshots/{summary['source']}` by "
             "`ablations/snapshots/make_summaries.py`.", "",
             "Persistence is the downstream affiliated share conditional on an "
             "affiliated first file (A1).", ""]
    reported = summary["reported_scope"]
    for scope in sorted(summary["scopes"], key=lambda s: s != reported):
        tag = " (reported in the paper)" if scope == reported else ""
        lines += [f"## Attempt scope: `{scope}`{tag}", "",
                  "| Model | Full disclosure | Staged disclosure |", "| --- | --- | --- |"]
        for model, row in summary["scopes"][scope].items():
            full = row.get("full_disclosure")
            staged = row.get("staged_disclosure")
            if not (full and staged):
                continue
            lines.append(
                f"| `{model}` | {full['conditional_persistence_pct']}% "
                f"[{full['ci95'][0]}, {full['ci95'][1]}] | "
                f"{staged['conditional_persistence_pct']}% "
                f"[{staged['ci95'][0]}, {staged['ci95'][1]}] |")
        lines.append("")
    lines += ["In the staged condition each file is requested in a fresh conversation "
              "with future tasks withheld, so persistence cannot come from advance "
              "planning over the full task list. `first_attempt` counts first attempts "
              "only; `latest_finished_attempt` counts each run at its last finished "
              "attempt, after timeout retries.", ""]
    return "\n".join(lines)


def write(ablation: str, summary: dict, markdown: str) -> None:
    out = TABLES / ablation
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out / "summary.md").write_text(markdown)
    print(f"wrote outputs/tables/{ablation}/summary.{{json,md}}")


def main() -> None:
    name = "assigned_as_code"
    summary = build_anchor_summary(SNAPSHOT_KEYS[name])
    write(name, summary, md_anchor("Assigned initial provider", summary))

    name = "single_shot_multifile"
    summary = build_a2_summary()
    write(name, summary, md_a2(summary))

    name = "by_instruction"
    summary = build_anchor_summary(SNAPSHOT_KEYS[name])
    write(name, summary, md_anchor("Instructed initial-provider choice", summary))

    name = "task_disclosure"
    summary = build_a4_summary()
    write(name, summary, md_a4(summary))


if __name__ == "__main__":
    main()
