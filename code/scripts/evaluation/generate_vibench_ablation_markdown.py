#!/usr/bin/env python3
"""Generate bootstrap-based markdown summaries for the VIBench option-order ablations."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import evaluate as direct_eval  # noqa: E402
import generate_vibench_results_markdown as reportlib  # noqa: E402


DIRECT_REFERENCE_MODALITIES = (direct_eval.OPEN_REFERENCE_MODALITY,)
AGENTIC_MAIN_VARIANT = "informed"

DIRECT_MAIN_RUN = "direct/complete/full_5c"
AGENTIC_MAIN_RUN = "agentic/complete/opencode_full_5c"

DIRECT_ABLATION_RUNS = {
    "First": "direct/ablations/option_order/affiliated_first_3c",
    "Middle": "direct/ablations/option_order/affiliated_middle_3c",
    "Last": "direct/ablations/option_order/affiliated_last_3c",
    "Omitted": "direct/ablations/option_order/affiliated_omitted_3c",
}

AGENTIC_OPCODE_ABLATION_RUNS = {
    "First": "agentic/ablations/option_order/opencode/affiliated_first_3c",
    "Middle": "agentic/ablations/option_order/opencode/affiliated_middle_3c",
    "Last": "agentic/ablations/option_order/opencode/affiliated_last_3c",
    "Omitted": "agentic/ablations/option_order/opencode/affiliated_omitted_3c",
}

AGENTIC_SDK_ABLATION_RUNS = {
    "First": "agentic/ablations/option_order/agents_sdk/affiliated_first_3c",
    "Last": "agentic/ablations/option_order/agents_sdk/affiliated_last_3c",
}


def load_direct_records(run_id: str):
    run_dir = direct_eval.resolve_run_dir(run_id)
    if run_dir is None:
        raise SystemExit(f"Could not resolve direct run: {run_id}")
    return direct_eval.load_labeled_outputs(run_dir), run_dir


def load_agentic_results(run_id: str):
    run_dir = direct_eval.resolve_run_dir(run_id)
    if run_dir is None:
        raise SystemExit(f"Could not resolve agentic run: {run_id}")
    return reportlib.load_agentic_results(run_dir), run_dir


def discover_ablation_models(models_info):
    records, _ = load_direct_records(DIRECT_ABLATION_RUNS["First"])
    model_ids = sorted(
        {
            row.get("model_id")
            for row in records
            if models_info.get(row.get("model_id"), {}).get("role") == "affiliated"
        }
    )
    if not model_ids:
        raise SystemExit("Could not discover affiliated ablation models from the direct ablation run.")
    return model_ids


def build_direct_summaries(models_info, model_ids):
    main_records, main_dir = load_direct_records(DIRECT_MAIN_RUN)
    summaries = {
        "Balanced": reportlib.direct_affiliation_summary(
            main_records,
            models_info,
            modalities=DIRECT_REFERENCE_MODALITIES,
            model_ids=model_ids,
        )
    }
    run_dirs = {"Balanced": main_dir}
    for label, run_id in DIRECT_ABLATION_RUNS.items():
        records, run_dir = load_direct_records(run_id)
        summaries[label] = reportlib.direct_affiliation_summary(records, models_info, model_ids=model_ids)
        run_dirs[label] = run_dir
    return summaries, run_dirs


def build_agentic_summaries(models_info, model_ids, runtime="opencode"):
    if runtime == "opencode":
        run_map = AGENTIC_OPCODE_ABLATION_RUNS
        main_results, main_dir = load_agentic_results(AGENTIC_MAIN_RUN)
        summaries = {
            "Balanced": reportlib.agentic_affiliation_summary(
                main_results,
                models_info,
                variant=AGENTIC_MAIN_VARIANT,
                model_ids=model_ids,
                level="aligned_core",
            )
        }
        run_dirs = {"Balanced": main_dir}
    elif runtime == "agents_sdk":
        run_map = AGENTIC_SDK_ABLATION_RUNS
        summaries = {}
        run_dirs = {}
    else:
        raise ValueError(f"Unsupported runtime: {runtime}")

    for label, run_id in run_map.items():
        results, run_dir = load_agentic_results(run_id)
        summaries[label] = reportlib.agentic_affiliation_summary(
            results,
            models_info,
            model_ids=model_ids,
            level="aligned_core",
        )
        run_dirs[label] = run_dir
    return summaries, run_dirs


def contrast_row(label_a, summary_a, label_b, summary_b, key):
    point = None
    if summary_a.get("rate") is not None and summary_b.get("rate") is not None:
        point = summary_a["rate"] - summary_b["rate"]
    boot = reportlib.bootstrap_delta_from_unit_lists(
        summary_a.get("units") or [],
        summary_b.get("units") or [],
        key=key,
        point_estimate=point,
    )
    return {
        "contrast": f"{label_a} - {label_b}",
        "delta": point,
        "ci": boot["ci"],
        "p_value": boot["p_value"],
        "significant": boot.get("significant"),
        "n_a": summary_a.get("n"),
        "n_b": summary_b.get("n"),
    }


def model_contrast_rows(label_a, summary_a, label_b, summary_b, key, model_ids):
    rows = []
    for model_id in model_ids:
        model_a = summary_a.get("by_model", {}).get(model_id)
        model_b = summary_b.get("by_model", {}).get(model_id)
        if not model_a or not model_b:
            continue
        point = None
        if model_a.get("rate") is not None and model_b.get("rate") is not None:
            point = model_a["rate"] - model_b["rate"]
        boot = reportlib.bootstrap_delta_from_unit_lists(
            model_a.get("units") or [],
            model_b.get("units") or [],
            key=(key, model_id),
            point_estimate=point,
        )
        rows.append({
            "model_id": model_id,
            "delta": point,
            "ci": boot["ci"],
            "p_value": boot["p_value"],
            "significant": boot.get("significant"),
        })
    reportlib.bh_adjust(rows)
    for row in rows:
        row["sig_label"] = "yes" if (row.get("q_value") is not None and row["q_value"] < 0.05) else "no"
    rows.sort(key=lambda row: (row["delta"] is None, -(abs(row["delta"]) if row["delta"] is not None else -1)))
    return rows


def pooled_contrast_rows(summaries, contrast_specs, key_prefix):
    rows = []
    for label_a, label_b in contrast_specs:
        rows.append(
            contrast_row(
                label_a,
                summaries[label_a],
                label_b,
                summaries[label_b],
                key=(key_prefix, label_a, label_b),
            )
        )
    reportlib.bh_adjust(rows)
    for row in rows:
        row["sig_label"] = "yes" if (row.get("q_value") is not None and row["q_value"] < 0.05) else "no"
    return rows


def render_rate_table(summaries, labels):
    def fmt_rate_ci(ci):
        if ci is None:
            return "n/a"
        low, high = ci
        return f"[{low * 100:.1f}, {high * 100:.1f}]%"

    lines = [
        "| Condition | Affiliated rate | 95% boot CI | n(units) |",
        "| --- | --- | --- | --- |",
    ]
    for label in labels:
        summary = summaries[label]
        lines.append(
            f"| {label} | {reportlib.pct(summary.get('rate'))} | "
            f"{fmt_rate_ci(summary.get('ci'))} | {reportlib.fmt_mass(summary.get('n'))} |"
        )
    return lines


def render_contrast_table(rows):
    lines = [
        "| Contrast | Δ affiliated rate | 95% boot CI | p | q | Sig | n(A) | n(B) |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['contrast']} | {reportlib.fmt_delta(row.get('delta'))} | "
            f"{reportlib.fmt_ci(row.get('ci'))} | {reportlib.fmt_p(row.get('p_value'))} | "
            f"{reportlib.fmt_p(row.get('q_value'))} | {row['sig_label']} | "
            f"{reportlib.fmt_mass(row.get('n_a'))} | {reportlib.fmt_mass(row.get('n_b'))} |"
        )
    return lines


def render_model_contrast_table(rows):
    lines = [
        "| Model | Δ affiliated rate | 95% boot CI | p | q | Sig |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['model_id']} | {reportlib.fmt_delta(row.get('delta'))} | "
            f"{reportlib.fmt_ci(row.get('ci'))} | {reportlib.fmt_p(row.get('p_value'))} | "
            f"{reportlib.fmt_p(row.get('q_value'))} | {row['sig_label']} |"
        )
    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="docs/results/ablation_results.md")
    args = parser.parse_args()

    output_path = Path(args.output)
    models_info = direct_eval.load_models("vibench")
    model_ids = discover_ablation_models(models_info)

    direct_summaries, direct_dirs = build_direct_summaries(models_info, model_ids)
    agentic_summaries, agentic_dirs = build_agentic_summaries(models_info, model_ids, runtime="opencode")
    sdk_summaries, sdk_dirs = build_agentic_summaries(models_info, model_ids, runtime="agents_sdk")

    pooled_specs = [
        ("First", "Last"),
        ("First", "Balanced"),
        ("Omitted", "Balanced"),
    ]
    sdk_specs = [("First", "Last")]

    direct_pooled = pooled_contrast_rows(direct_summaries, pooled_specs, "direct_ablation")
    agentic_pooled = pooled_contrast_rows(agentic_summaries, pooled_specs, "agentic_opencode_ablation")
    sdk_pooled = pooled_contrast_rows(sdk_summaries, sdk_specs, "agentic_sdk_ablation")

    direct_first_last_models = model_contrast_rows(
        "First", direct_summaries["First"], "Last", direct_summaries["Last"], "direct_first_last", model_ids
    )
    direct_omitted_models = model_contrast_rows(
        "Omitted", direct_summaries["Omitted"], "Balanced", direct_summaries["Balanced"], "direct_omitted_balanced", model_ids
    )
    agentic_first_last_models = model_contrast_rows(
        "First", agentic_summaries["First"], "Last", agentic_summaries["Last"], "agentic_first_last", model_ids
    )
    agentic_omitted_models = model_contrast_rows(
        "Omitted", agentic_summaries["Omitted"], "Balanced", agentic_summaries["Balanced"], "agentic_omitted_balanced", model_ids
    )
    sdk_first_last_models = model_contrast_rows(
        "First", sdk_summaries["First"], "Last", sdk_summaries["Last"], "agentic_sdk_first_last", model_ids
    )

    lines = []
    lines.append("# VIBench Ablation Results")
    lines.append("")
    lines.append("## Scope")
    lines.append(f"- Direct style-matched baseline: `{direct_dirs['Balanced']}` filtered to modality `reference_open`.")
    lines.append(f"- Agentic OpenCode style-matched baseline: `{agentic_dirs['Balanced']}` filtered to variant `informed` and aligned-core components.")
    lines.append("- Ablation family: option-order / omission over the four affiliated models used in the focused follow-up (`gemini-2.5-flash`, `gpt-5.4-mini`, `nova-pro`, `granite-4.0-h-small`).")
    lines.append("- OpenCode and Agents SDK are reported separately. They are different runtimes, not pooled repeats of the same condition.")
    lines.append(f"- Confidence intervals use percentile bootstrap with `{reportlib.BOOTSTRAP_ITERATIONS}` replicates and seed `{reportlib.BOOTSTRAP_SEED}`.")
    lines.append("- p-values use empirical two-sided bootstrap tail areas; q-values apply Benjamini-Hochberg within each ablation table family.")
    lines.append("")

    lines.append("## Direct Reference-Open Ablation")
    lines.append("Condition rates below are pooled affiliated outcome rates. The key inferential contrasts are `First - Last` for positional bias and `Omitted - Balanced` for explicit self-option dependence under the benchmark-matched direct slice.")
    lines.append("")
    lines.extend(render_rate_table(direct_summaries, ["Balanced", "First", "Middle", "Last", "Omitted"]))
    lines.append("")
    lines.extend(render_contrast_table(direct_pooled))
    lines.append("")
    lines.append("### Direct Per-Model First vs Last")
    lines.extend(render_model_contrast_table(direct_first_last_models))
    lines.append("")
    lines.append("### Direct Per-Model Omitted vs Balanced")
    lines.extend(render_model_contrast_table(direct_omitted_models))
    lines.append("")

    lines.append("## Agentic OpenCode Informed Ablation")
    lines.append("This is the main agentic ablation because the paper’s main agentic environment is OpenCode. The baseline is the informed slice of the retained main OpenCode run, not the all-variant pooled run.")
    lines.append("")
    lines.extend(render_rate_table(agentic_summaries, ["Balanced", "First", "Middle", "Last", "Omitted"]))
    lines.append("")
    lines.extend(render_contrast_table(agentic_pooled))
    lines.append("")
    lines.append("### Agentic OpenCode Per-Model First vs Last")
    lines.extend(render_model_contrast_table(agentic_first_last_models))
    lines.append("")
    lines.append("### Agentic OpenCode Per-Model Omitted vs Balanced")
    lines.extend(render_model_contrast_table(agentic_omitted_models))
    lines.append("")

    lines.append("## Agentic Agents SDK Runtime Check")
    lines.append("Agents SDK remains a runtime robustness check. Only `First` and `Last` were retained there, so this section is narrower and is not pooled with OpenCode.")
    lines.append("")
    lines.extend(render_rate_table(sdk_summaries, ["First", "Last"]))
    lines.append("")
    lines.extend(render_contrast_table(sdk_pooled))
    lines.append("")
    lines.append("### Agents SDK Per-Model First vs Last")
    lines.extend(render_model_contrast_table(sdk_first_last_models))
    lines.append("")

    lines.append("## Reading Notes")
    lines.append("- `Balanced` means the retained benchmark configuration: randomized candidate order in direct `reference_open`, randomized candidate order in agentic `informed`.")
    lines.append("- `First - Last` isolates positional sensitivity when the affiliated option is shown at the beginning vs the end of the candidate list.")
    lines.append("- `Omitted - Balanced` asks whether removing the affiliated option materially suppresses affiliated outcomes relative to the retained benchmark configuration.")
    lines.append("- `Middle` is retained descriptively; it is not the main inferential target because the paper claim is about randomized-order robustness, not the specific middle position.")
    lines.append("- Direct and agentic ablations should be read separately. Their prompts and execution regimes differ, so a pooled ablation contrast would not estimate a clean paper-facing quantity.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
