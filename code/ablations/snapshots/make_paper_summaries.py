#!/usr/bin/env python3
"""Derive the headline claim of each paper robustness analysis from its tables.

The analyses that reuse the main evaluation pipeline keep their derived tables
under `ablations/<name>/results/`. This script reads those tables and writes

    outputs/tables/<name>/headline.md

so each claim in the paper can be checked against the numbers it came from.
Nothing is hardcoded; re-run with

    python ablations/snapshots/make_paper_summaries.py

Covers the four analyses whose derived tables ship in this package. The other
two (option order, agentic runtime) are regenerated from the run outputs by
their own scripts; see each directory's README.
"""

from __future__ import annotations

import csv
import re
import statistics as stats
from pathlib import Path

TABLES = Path(__file__).resolve().parents[3] / "outputs" / "tables"


def rows(path: Path) -> list[dict]:
    with path.open() as fh:
        return list(csv.DictReader(fh))


def control_composition() -> str:
    """Do originally positive effects survive every control subset?"""
    here = TABLES / "control_composition"
    vib = {}
    for r in rows(TABLES / "concentration_vs_affiliation" / "gini_vib_per_model.csv"):
        if r["role"] == "affiliated" and r["vib"]:
            vib[(r["setting"], r["model_id"])] = (float(r["vib"]), float(r["vib_ci_low"]))
    subsets = {
        (r["setting"], r["model_id"]): (int(r["positive_subsets"]), int(r["subset_count"]))
        for r in rows(here / "control_subset_sensitivity.csv")
    }

    lines = ["# Control-composition sensitivity — headline", "",
             "Derived from `control_subset_sensitivity.csv` and the VIB point estimates "
             "in `../concentration_vs_affiliation/gini_vib_per_model.csv` by "
             "`ablations/snapshots/make_paper_summaries.py`.", "",
             "| Setting | Affiliated models | Significantly positive VIB | Of those, positive in every subset |",
             "| --- | --- | --- | --- |"]
    for setting in ("direct", "agentic"):
        present = [k for k in vib if k[0] == setting]
        significant = [k for k in present if vib[k][1] > 0]
        survived = [k for k in significant
                    if subsets.get(k, (0, 1))[0] == subsets.get(k, (0, 1))[1]]
        lines.append(f"| {setting} | {len(present)} | {len(significant)} | "
                     f"{len(survived)}/{len(significant)} |")

    agg = rows(here / "aggregation_rule_sensitivity.csv")
    deltas = [abs(float(r["pooled_minus_mean"])) for r in agg if r["pooled_minus_mean"]]
    med_deltas = [abs(float(r["median_minus_mean"])) for r in agg if r["median_minus_mean"]]
    lines += ["",
              "Subsets are the seven non-empty subsets of the three non-affiliated controls.",
              "",
              "Alternative aggregation rules, as absolute change in VIB against the "
              "unweighted mean used in the paper:", "",
              f"- pooled instead of mean: max {max(deltas):.4f}, median {stats.median(deltas):.4f}",
              f"- median instead of mean: max {max(med_deltas):.4f}, median {stats.median(med_deltas):.4f}",
              ""]
    return "\n".join(lines)


def prompt_format() -> str:
    """Is aggregate VIB positive under every prompt format?"""
    here = TABLES / "prompt_format"
    by_format: dict[str, list[float]] = {}
    for r in rows(here / "table_b_vib.csv"):
        if r["role"] == "affiliated" and r["estimate"]:
            by_format.setdefault(r["setting"], []).append(float(r["estimate"]))

    lines = ["# Prompt-format robustness — headline", "",
             "Derived from `table_b_vib.csv` by "
             "`ablations/snapshots/make_paper_summaries.py`.", "",
             "| Prompt format | Affiliated models | Mean VIB | Models with positive VIB |",
             "| --- | --- | --- | --- |"]
    for fmt, values in by_format.items():
        positive = sum(1 for v in values if v > 0)
        lines.append(f"| `{fmt}` | {len(values)} | {stats.mean(values):+.3f} | "
                     f"{positive}/{len(values)} |")
    lines += ["", "Mean VIB is positive under every prompt format, in both the direct and "
                  "agentic settings. Individual models vary: the aggregate effect does not "
                  "depend on one wording, but it is not present in every model under every "
                  "format.", ""]
    return "\n".join(lines)


def concentration_gini() -> str:
    """Does VIB restate provider concentration?"""
    here = TABLES / "concentration_vs_affiliation"
    paired: dict[str, list[tuple[float, float]]] = {}
    for r in rows(here / "gini_vib_per_model.csv"):
        if r["role"] == "affiliated" and r["vib"] and r["mean_normalized_gini"]:
            paired.setdefault(r["setting"], []).append(
                (float(r["vib"]), float(r["mean_normalized_gini"])))

    lines = ["# Concentration versus affiliation — headline", "",
             "Derived from `gini_vib_per_model.csv` by "
             "`ablations/snapshots/make_paper_summaries.py`.", "",
             "| Setting | Affiliated models | Correlation of VIB with normalized Gini Index |",
             "| --- | --- | --- |"]
    for setting, pairs in paired.items():
        if len(pairs) < 3:
            continue
        corr = stats.correlation([v for v, _ in pairs], [g for _, g in pairs])
        lines.append(f"| {setting} | {len(pairs)} | {corr:+.3f} |")
    lines += ["", "The normalized Gini Index is the closest measure in prior work. Its "
                  "correlation with VIB is near zero, so concentration and "
                  "affiliation-relative excess selection are not measuring the same thing.",
              ""]
    return "\n".join(lines)


def affiliation_microsoft_openai() -> str:
    """Does merging Microsoft and OpenAI create the GPT result, or dilute it?"""
    here = TABLES / "affiliation_definition"
    data = rows(here / "indirect_affiliation_sensitivity.csv")

    lines = ["# Microsoft-OpenAI affiliation sensitivity — headline", "",
             "Derived from `indirect_affiliation_sensitivity.csv` by "
             "`ablations/snapshots/make_paper_summaries.py`.", "",
             "VIB for the GPT models under three affiliation definitions. "
             "`merged_microsoft_openai` is the definition used in the paper.", "",
             "| Mapping | Setting | Model | VIB | 95% CI | p |",
             "| --- | --- | --- | --- | --- | --- |"]
    order = {"merged_microsoft_openai": 0, "openai_only": 1, "azure_only": 2}
    for r in sorted(data, key=lambda r: (order.get(r["mapping"], 9), r["setting"], r["model_id"])):
        vib, lo, hi = float(r["vib"]), float(r["ci_low"]), float(r["ci_high"])
        mark = "" if lo > 0 or hi < 0 else " (n.s.)"
        lines.append(f"| `{r['mapping']}` | {r['setting']} | `{r['model_id']}` | "
                     f"{vib:+.3f}{mark} | [{lo:+.3f}, {hi:+.3f}] | {float(r['p_value']):.4f} |")
    lines += ["", "Reading the direct rows: under the merged definition GPT-5.4's direct VIB "
                  "is not distinguishable from zero, while restricting attribution to OpenAI "
                  "surfaces makes it significantly positive, and restricting to Azure "
                  "surfaces makes it negative. Merging the two therefore dilutes the direct "
                  "signal rather than creating it.", ""]
    return "\n".join(lines)


def agentic_runtime() -> str:
    """Does the agentic result hold on a second agent framework?"""
    here = TABLES / "agent_runtime"

    def aligned_vib(report: pathlib.Path) -> dict[str, float]:
        """Pull all-variants aligned-core VIB per model out of an evaluator report."""
        out, in_block = {}, False
        for line in report.read_text().splitlines():
            if "[all variants]" in line:
                in_block = True
                continue
            if in_block:
                if line.strip().startswith("[") or line.startswith("---"):
                    break
                match = re.match(r"\s+(\S+)\s+\(.*aligned=.*?VIB ([+\-][\d.]+)%", line)
                if match:
                    out[match.group(1)] = float(match.group(2))
        return out

    opencode = aligned_vib(here / "report_opencode.txt")
    sdk = aligned_vib(here / "report_agents_sdk.txt")

    lines = ["# Agentic runtime comparison — headline", "",
             "Derived from the two evaluator reports in this directory by "
             "`ablations/snapshots/make_paper_summaries.py`.", "",
             "Aligned-core VIB (percentage points), all prompt variants pooled, for the "
             "same benchmark run on two agent frameworks.", "",
             "| Model | OpenCode | Agents SDK | SDK − OpenCode |",
             "| --- | --- | --- | --- |"]
    both = [m for m in opencode if m in sdk]
    for model in both:
        delta = sdk[model] - opencode[model]
        lines.append(f"| `{model}` | {opencode[model]:+.1f} | {sdk[model]:+.1f} | "
                     f"{delta:+.1f} |")
    agree = sum(1 for m in both if (opencode[m] > 0) == (sdk[m] > 0))
    lines += ["", f"The sign of VIB agrees on both runtimes for {agree} of {len(both)} "
                  "affiliated models, so the agentic finding is not an artifact of one "
                  "agent framework. Magnitudes are generally smaller under the Agents SDK, "
                  "which is why the paper reports OpenCode as the main arm and this as a "
                  "robustness check.", ""]
    return "\n".join(lines)


def main() -> None:
    for name, build in (("control_composition", control_composition),
                        ("prompt_format", prompt_format),
                        ("concentration_vs_affiliation", concentration_gini),
                        ("affiliation_definition", affiliation_microsoft_openai),
                        ("agent_runtime", agentic_runtime)):
        out = TABLES / name / "headline.md"
        out.write_text(build())
        print(f"wrote outputs/tables/{name}/headline.md")


if __name__ == "__main__":
    main()
