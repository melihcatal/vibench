#!/usr/bin/env python3
"""
Generate compact appendix LaTeX tables from the paper-facing results.

The appendix is intentionally restricted to two publishable tables:
1. Raw direct and agentic ecosystem selection rates
2. Main affiliated-model VIB results
3. Prompt-format VIB results
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from collections import Counter, defaultdict


DIRECT_MODEL_ORDER = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gpt-5.4",
    "gpt-5.4-mini",
    "nova-pro",
    "nova-2-lite",
    "granite-4.0-h-small",
    "granite-4.0-h-tiny-local",
    "qwen3.6-plus",
    "qwen3-coder-flash",
    "deepseek-v3.2",
    "mistral-large-3",
    "grok-4-1-fast-reasoning",
]

ADJUSTED_MODEL_ORDER = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gpt-5.4",
    "gpt-5.4-mini",
    "nova-pro",
    "nova-2-lite",
    "granite-4.0-h-small",
    "granite-4.0-h-tiny-local",
    "qwen3.6-plus",
    "qwen3-coder-flash",
]

PROVIDER_LABELS = {
    "google": "Google",
    "Microsoft/OpenAI": r"OpenAI\openaiindirectmark",
    "aws": "AWS",
    "ibm": "IBM",
    "alibaba": "Alibaba",
    "independent": "Independent",
}

MODEL_LABELS = {
    "gemini-2.5-flash": "Gemini 2.5 Flash",
    "gemini-2.5-pro": "Gemini 2.5 Pro",
    "gpt-5.4": "GPT-5.4",
    "gpt-5.4-mini": "GPT-5.4 Mini",
    "nova-pro": "Nova Pro",
    "nova-2-lite": "Nova-2 Lite",
    "granite-4.0-h-small": "Granite 4.0 H Small",
    "granite-4.0-h-tiny-local": "Granite 4.0 H Tiny",
    "qwen3.6-plus": "Qwen 3.6 Plus",
    "qwen3-coder-flash": "Qwen3 Coder Flash",
    "deepseek-v3.2": "DeepSeek V3.2",
    "mistral-large-3": "Mistral Large 3",
    "grok-4-1-fast-reasoning": "Grok-4.1 Fast Reasoning",
}

PROVIDER_ORDER = [
    "google",
    "Microsoft/OpenAI",
    "aws",
    "ibm",
    "alibaba",
    "independent",
]

CONTROL_MODELS = {
    "deepseek-v3.2",
    "mistral-large-3",
    "grok-4-1-fast-reasoning",
}

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import evaluate as direct_eval  # noqa: E402
import generate_vibench_results_markdown as reportlib  # noqa: E402

AGENTIC_RESULTS_PATH = REPO_ROOT / "outputs" / "runs" / "agentic" / "complete" / "opencode_full_5c" / "labeled" / "agentic" / "results.json"
DIRECT_LABELED_PATH = REPO_ROOT / "outputs" / "runs" / "direct" / "complete" / "full_5c" / "labeled"
DIRECT_TASKS_PATH = REPO_ROOT / "benchmark" / "vibench" / "direct" / "tasks.jsonl"
AGENTIC_TASKS_PATH = REPO_ROOT / "benchmark" / "vibench" / "agentic" / "tasks.jsonl"


@dataclass
class HeadingNode:
    level: int
    title: str
    paragraphs: list[str] = field(default_factory=list)
    table: list[list[str]] | None = None
    children: list["HeadingNode"] = field(default_factory=list)


def escape_latex(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def parse_markdown(md_text: str) -> list[HeadingNode]:
    roots: list[HeadingNode] = []
    stack: list[HeadingNode] = []
    lines = md_text.splitlines()
    i = 0

    def current_node() -> HeadingNode | None:
        return stack[-1] if stack else None

    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            node = HeadingNode(level=2, title=line[3:].strip())
            roots.append(node)
            stack = [node]
            i += 1
            continue
        if line.startswith("### "):
            node = HeadingNode(level=3, title=line[4:].strip())
            while stack and stack[-1].level >= 3:
                stack.pop()
            if stack:
                stack[-1].children.append(node)
            stack.append(node)
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines) and lines[i + 1].startswith("| ---"):
            raw_rows = []
            while i < len(lines) and lines[i].startswith("|"):
                raw_rows.append(lines[i])
                i += 1
            table = parse_markdown_table(raw_rows)
            node = current_node()
            if node:
                node.table = table
            continue
        stripped = line.strip()
        if stripped and not stripped.startswith("!["):
            node = current_node()
            if node:
                node.paragraphs.append(stripped)
        i += 1
    return roots


def parse_markdown_table(lines: list[str]) -> list[list[str]]:
    rows = []
    for idx, line in enumerate(lines):
        if idx == 1:
            continue
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def table_to_dicts(table: list[list[str]]) -> list[dict[str, str]]:
    headers = table[0]
    return [dict(zip(headers, row)) for row in table[1:]]


def get_root_map(md_path: Path) -> dict[str, HeadingNode]:
    roots = parse_markdown(md_path.read_text())
    return {node.title: node for node in roots}


def child_table(root_map: dict[str, HeadingNode], root_title: str, child_title: str) -> list[dict[str, str]]:
    root = root_map[root_title]
    for child in root.children:
        if child.title == child_title and child.table:
            return table_to_dicts(child.table)
    raise KeyError(f"Missing child table: {root_title} / {child_title}")


def root_table(root_map: dict[str, HeadingNode], root_title: str) -> list[dict[str, str]]:
    root = root_map[root_title]
    if not root.table:
        raise KeyError(f"Missing root table: {root_title}")
    return table_to_dicts(root.table)


def provider_key(affil: str) -> str:
    if affil in {"n/a", "control", "independent"}:
        return "independent"
    if affil == "google":
        return "google"
    if affil == "Microsoft/OpenAI":
        return "Microsoft/OpenAI"
    if affil == "aws":
        return "aws"
    if affil == "ibm":
        return "ibm"
    if affil == "alibaba":
        return "alibaba"
    return affil


def provider_groups(rows: list[dict[str, str]]) -> list[tuple[str, list[dict[str, str]]]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        key = row["provider"]
        grouped.setdefault(key, []).append(row)
    return [(key, grouped[key]) for key in PROVIDER_ORDER if key in grouped]


def normalize_value(text: str) -> str:
    return text.replace("-0.0pp", "0.0pp").replace("+0.0pp", "0.0pp").replace("-0.0", "0.0").replace("+0.0", "0.0")


def strip_count_suffix(text: str) -> str:
    text = text.strip()
    if " (n=" in text and text.endswith(")"):
        return text.split(" (n=", 1)[0]
    return text


def strip_unit(text: str) -> str:
    text = normalize_value(strip_count_suffix(text)).strip()
    if text.endswith("%"):
        return text[:-1]
    if text.endswith("pp"):
        return text[:-2]
    return text


def to_float(text: str) -> float | None:
    text = strip_unit(text)
    if text in {"", "--"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


AFFILIATED_DIRECT_KEY = {
    "google": "google",
    "Microsoft/OpenAI": "msoai",
    "aws": "aws",
    "ibm": "ibm",
    "alibaba": "alibaba",
}

PANEL_HEADERS = {
    "aws": "AWS",
    "google": "Google",
    "msoai": "MS/OAI",
    "ibm": "IBM",
    "alibaba": "Ali.",
    "indep": "Indep.",
}

RAW_DIRECT_KEYS = ["aws", "google", "msoai", "ibm", "alibaba", "indep"]
RAW_AGENTIC_KEYS = ["agt_aws", "agt_google", "agt_msoai", "agt_ibm", "agt_alibaba", "agt_indep"]

DIRECT_PROMPT_FORMATS = [
    ("nli", "NLI"),
    ("fim", "FIM"),
    ("reference_open", "Reference-Open"),
]

AGENTIC_PROMPT_FORMATS = [
    ("Free: Aligned Core", "NLI"),
    ("Informed: Aligned Core", "Reference-Open"),
]

AFFIL_TO_ECOSYSTEM = {
    "google": "google",
    "Microsoft/OpenAI": "microsoft_openai",
    "aws": "aws",
    "ibm": "ibm",
    "alibaba": "alibaba",
}


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    seen = set()
    ordered = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def _ecosystem_values_from_component(component: dict) -> list[str]:
    raw_values = component.get("detected_ecosystems")
    if isinstance(raw_values, list):
        values = _dedupe_preserve_order(raw_values)
    elif raw_values:
        values = [raw_values]
    else:
        values = []
    if not values:
        values = [component.get("ecosystem") or "unknown"]
    return values


def _ecosystem_share_pairs(component: dict) -> list[tuple[str, float]]:
    values = _ecosystem_values_from_component(component)
    weight = 1.0 / len(values) if values else 1.0
    return [(value, weight) for value in values] if values else [("unknown", 1.0)]


def _ecosystem_share(record: dict, ecosystem: str) -> float:
    values = _ecosystem_values_from_component(record)
    if not values:
        return 0.0
    return sum(1 for value in values if value == ecosystem) / len(values)


def table_ecosystem_key(ecosystem: str) -> str | None:
    if ecosystem == "aws":
        return "aws"
    if ecosystem == "google":
        return "google"
    if ecosystem == "microsoft_openai":
        return "msoai"
    if ecosystem == "ibm":
        return "ibm"
    if ecosystem == "alibaba":
        return "alibaba"
    if ecosystem == "unknown":
        return None
    return "indep"


def compute_agentic_aligned_rates(results_path: Path) -> dict[str, dict[str, str]]:
    with results_path.open() as f:
        results = json.load(f)

    totals = defaultdict(float)
    counts = defaultdict(Counter)
    for row in results:
        model_id = row["model_id"]
        for comp in row.get("components", {}).values():
            if comp.get("component_group") != "aligned_core":
                continue
            totals[model_id] += 1
            for ecosystem, weight in _ecosystem_share_pairs(comp):
                key = table_ecosystem_key(ecosystem)
                if key is None:
                    continue
                counts[model_id][key] += weight

    out = {}
    for model_id in DIRECT_MODEL_ORDER:
        total = totals.get(model_id, 0.0)
        row = {}
        for key in RAW_DIRECT_KEYS:
            if total <= 0:
                row[f"agt_{key}"] = "--"
            else:
                row[f"agt_{key}"] = f"{100.0 * counts[model_id].get(key, 0.0) / total:.1f}"
        out[model_id] = row
    return out


def format_panel_cell(row: dict[str, str], key: str, panel_keys: list[str]) -> str:
    text = strip_unit(row.get(key, "--"))
    display = escape_latex(text)
    vals = {k: to_float(row.get(k, "--")) for k in panel_keys}
    present = [v for v in vals.values() if v is not None]
    if present:
        row_max = max(present)
        if vals.get(key) is not None and abs(vals[key] - row_max) < 1e-9:
            return rf"\textbf{{{display}}}"
    return display
def format_metric_cell(text: str) -> str:
    return escape_latex(strip_unit(text))


def significance_marker(q_text: str) -> str:
    q_val = to_float(q_text)
    if q_val is None:
        return ""
    if q_val < 0.05:
        return r"$^{*}$"
    return ""


def format_pq(value: str | float | None) -> str:
    if value is None:
        return "--"
    if isinstance(value, str):
        if value.strip() in {"", "--", "n/a"}:
            return "--"
        try:
            numeric = float(value)
        except ValueError:
            return escape_latex(value)
    else:
        numeric = float(value)
    return f"{numeric:.4f}"


def format_vib_cell(value_text: str, q_text: str) -> str:
    return f"{format_metric_cell(value_text)}{significance_marker(q_text)}"


def subtract_metric_strings(left: str, right: str) -> str:
    lval = to_float(left)
    rval = to_float(right)
    if lval is None or rval is None:
        return "--"
    diff = lval - rval
    return f"{diff:+.1f}"


def _load_direct_records(modality: str) -> list[dict]:
    modality_dir = DIRECT_LABELED_PATH / modality
    records = []
    for path in sorted(modality_dir.rglob("*.json")):
        with path.open() as f:
            records.append(json.load(f))
    return records


def _scenario_rate(records_by_model_scenario: dict[tuple[str, str], list[dict]], model_id: str, scenario_id: str, ecosystem: str) -> float | None:
    records = records_by_model_scenario.get((model_id, scenario_id), [])
    if not records:
        return None
    return sum(_ecosystem_share(record, ecosystem) for record in records) / len(records)


def compute_direct_prompt_vib_rows(direct_vib: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    prompt_values: dict[str, dict[str, str]] = {model_id: {} for model_id in ADJUSTED_MODEL_ORDER}
    models_info = direct_eval.load_models("vibench")
    direct_run = direct_eval.resolve_run_dir("direct/complete/full_5c")
    direct_records = direct_eval.load_labeled_outputs(direct_run)

    for modality, _label in DIRECT_PROMPT_FORMATS:
        rows, _stats, _vib_map = reportlib.direct_matched_vib_rows(
            direct_records,
            models_info,
            modalities=(modality,),
            level="aligned_core",
            mode="share",
            bootstrap=True,
        )
        for row in rows:
            model_id = row["model_id"]
            if model_id not in prompt_values:
                continue
            prompt_values[model_id][modality] = f"{100.0 * row['vib']:+.1f}"
            prompt_values[model_id][f"{modality}_p"] = format_pq(row.get("p_value"))
            prompt_values[model_id][f"{modality}_q"] = format_pq(row.get("q_value"))

    return prompt_values


def render_prompt_format_table(rows: list[dict[str, str]]) -> str:
    lines = [
        r"\begin{center}",
        r"\centering",
        r"\tiny",
        r"\setlength{\tabcolsep}{2pt}",
        r"\renewcommand{\arraystretch}{1.08}",
        r"\captionof{table}{VIB by prompt format for provider-affiliated models. Direct columns report scenario-matched VIB within the NLI, FIM, and Reference-Open direct prompt formats. Agentic columns report aligned-core VIB for the matched NLI-style and Reference-Open-style agentic prompt formats. Values are percentage points relative to the matched strict-control baseline. We report bootstrap $p$-values and FDR-adjusted $q$-values; asterisks mark FDR-adjusted significance ($^{*}q<0.05$).}",
        r"\label{tab:appendix-prompt-format-vib}",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{>{\raggedright\arraybackslash}p{1.20cm} >{\raggedright\arraybackslash}p{2.05cm} *{5}{>{\centering\arraybackslash}p{0.70cm} >{\centering\arraybackslash}p{0.72cm} >{\centering\arraybackslash}p{0.72cm}}}",
        r"\toprule",
        r"\multirow{2}{*}{Provider} & \multirow{2}{*}{Model} & \multicolumn{9}{c}{Direct} & \multicolumn{6}{c}{Agentic} \\",
        r"\cmidrule(lr){3-11}\cmidrule(lr){12-17}",
        r"& & \multicolumn{3}{c}{NLI} & \multicolumn{3}{c}{FIM} & \multicolumn{3}{c}{Ref.-Open} & \multicolumn{3}{c}{NLI} & \multicolumn{3}{c}{Ref.-Open} \\",
        r"\cmidrule(lr){3-5}\cmidrule(lr){6-8}\cmidrule(lr){9-11}\cmidrule(lr){12-14}\cmidrule(lr){15-17}",
        r"& & VIB & $p$ & $q$ & VIB & $p$ & $q$ & VIB & $p$ & $q$ & VIB & $p$ & $q$ & VIB & $p$ & $q$ \\",
        r"\midrule",
    ]
    grouped = provider_groups(rows)
    for group_idx, (provider, group_rows) in enumerate(grouped):
        for idx, row in enumerate(group_rows):
            provider_cell = ""
            if idx == 0:
                provider_cell = rf"\multirow{{{len(group_rows)}}}{{*}}{{{PROVIDER_LABELS[provider]}}}"
            model = escape_latex(MODEL_LABELS[row["model_id"]])
            line = " & ".join([
                provider_cell,
                model,
                format_vib_cell(row["nli"], row["nli_q"]),
                row["nli_p"],
                row["nli_q"],
                format_vib_cell(row["fim"], row["fim_q"]),
                row["fim_p"],
                row["fim_q"],
                format_vib_cell(row["reference_open"], row["reference_open_q"]),
                row["reference_open_p"],
                row["reference_open_q"],
                format_vib_cell(row["free"], row["free_q"]),
                row["free_p"],
                row["free_q"],
                format_vib_cell(row["informed"], row["informed_q"]),
                row["informed_p"],
                row["informed_q"],
            ]) + r" \\"
            lines.append(line)
        if group_idx != len(grouped) - 1:
            lines.append(r"\midrule")
    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"}",
        r"\end{center}",
        "",
    ]
    return "\n".join(lines)


def render_raw_table(rows: list[dict[str, str]]) -> str:
    lines = [
        r"\begin{center}",
        r"\centering",
        r"\scriptsize",
        r"\setlength{\tabcolsep}{2pt}",
        r"\renewcommand{\arraystretch}{1.12}",
        r"\captionof{table}{Raw ecosystem selection rates for all evaluated models. For each provider ecosystem, the Direct subcolumn reports the direct ecosystem rate across all direct outputs, and the Agentic subcolumn reports the raw aligned-core ecosystem rate over $A1$--$A4$, which is the direct 1-to-1 counterpart of the four direct subtasks. All values are percentages. Bold marks the highest ecosystem rate within each setting; ties are bolded jointly.}",
        r"\label{tab:appendix-raw-rates}",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{>{\raggedright\arraybackslash}p{1.35cm} >{\raggedright\arraybackslash}p{2.55cm} *{12}{>{\centering\arraybackslash}p{0.62cm}}}",
        r"\toprule",
        r"\multirow{2}{*}{Provider} & \multirow{2}{*}{Model} & \multicolumn{2}{c}{AWS} & \multicolumn{2}{c}{Google} & \multicolumn{2}{c}{MS/OAI} & \multicolumn{2}{c}{IBM} & \multicolumn{2}{c}{Ali.} & \multicolumn{2}{c}{Indep.} \\",
        r"\cmidrule(lr){3-4}\cmidrule(lr){5-6}\cmidrule(lr){7-8}\cmidrule(lr){9-10}\cmidrule(lr){11-12}\cmidrule(lr){13-14}",
        r"& & Dir. & Agt. & Dir. & Agt. & Dir. & Agt. & Dir. & Agt. & Dir. & Agt. & Dir. & Agt. \\",
        r"\midrule",
    ]
    grouped = provider_groups(rows)
    for group_idx, (provider, group_rows) in enumerate(grouped):
        for idx, row in enumerate(group_rows):
            provider_cell = ""
            if idx == 0:
                provider_cell = rf"\multirow{{{len(group_rows)}}}{{*}}{{{PROVIDER_LABELS[provider]}}}"
            model = escape_latex(MODEL_LABELS[row["model_id"]])
            cells = []
            for direct_key, agentic_key in zip(RAW_DIRECT_KEYS, RAW_AGENTIC_KEYS):
                cells.append(format_panel_cell(row, direct_key, RAW_DIRECT_KEYS))
                cells.append(format_panel_cell(row, agentic_key, RAW_AGENTIC_KEYS))
            lines.append(" & ".join([provider_cell, model, *cells]) + r" \\")
        if group_idx != len(grouped) - 1:
            lines.append(r"\midrule")
    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"}",
        r"\end{center}",
        "",
    ]
    return "\n".join(lines)


def render_results_table(rows: list[dict[str, str]]) -> str:
    lines = [
        r"\begin{center}",
        r"\centering",
        r"\scriptsize",
        r"\setlength{\tabcolsep}{2pt}",
        r"\renewcommand{\arraystretch}{1.12}",
        r"\captionof{table}{VIB results for provider-affiliated models only. Direct VIB and Agentic VIB are the control-subtracted affiliated-preference metrics reported in the main paper, with agentic VIB computed on the aligned-core block $A1$--$A4$. We report percentile bootstrap 95\% confidence intervals, bootstrap $p$-values, and FDR-adjusted $q$-values. Asterisks on VIB values mark FDR-adjusted significance ($^{*}q<0.05$). $\Delta$ Transition denotes Agentic VIB minus Direct VIB and is shown descriptively here. VIB values and confidence intervals are in percentage points.}",
        r"\label{tab:appendix-main-results}",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{>{\raggedright\arraybackslash}p{1.25cm} >{\raggedright\arraybackslash}p{2.15cm} *{2}{>{\centering\arraybackslash}p{0.88cm} >{\centering\arraybackslash}p{1.85cm} >{\centering\arraybackslash}p{0.72cm} >{\centering\arraybackslash}p{0.72cm}} >{\centering\arraybackslash}p{1.00cm}}",
        r"\toprule",
        r"\multirow{2}{*}{Provider} & \multirow{2}{*}{Model} & \multicolumn{4}{c}{Direct} & \multicolumn{4}{c}{Agentic} & \multirow{2}{*}{$\Delta$ Transition} \\",
        r"\cmidrule(lr){3-6}\cmidrule(lr){7-10}",
        r"& & VIB & 95\% CI & $p$ & $q$ & VIB & 95\% CI & $p$ & $q$ & \\",
        r"\midrule",
    ]
    grouped = provider_groups(rows)
    for group_idx, (provider, group_rows) in enumerate(grouped):
        for idx, row in enumerate(group_rows):
            provider_cell = ""
            if idx == 0:
                provider_cell = rf"\multirow{{{len(group_rows)}}}{{*}}{{{PROVIDER_LABELS[provider]}}}"
            model = escape_latex(MODEL_LABELS[row["model_id"]])
            line = " & ".join([
                provider_cell,
                model,
                format_vib_cell(row["direct_vib"], row["direct_q"]),
                format_metric_cell(row["direct_ci"]),
                format_pq(row["direct_p"]),
                format_metric_cell(row["direct_q"]),
                format_vib_cell(row["agentic_vib"], row["agentic_q"]),
                format_metric_cell(row["agentic_ci"]),
                format_pq(row["agentic_p"]),
                format_metric_cell(row["agentic_q"]),
                format_metric_cell(row["transition_delta"]),
            ]) + r" \\"
            lines.append(line)
        if group_idx != len(grouped) - 1:
            lines.append(r"\midrule")
    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"}",
        r"\end{center}",
        "",
    ]
    return "\n".join(lines)


def direct_ordered_rows(raw_rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    row_map = {row["model_id"]: row for row in raw_rows}
    return [row_map[m] for m in DIRECT_MODEL_ORDER if m in row_map]


def adjusted_ordered_rows(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    row_map = {row["model_id"]: row for row in rows}
    return [row_map[m] for m in ADJUSTED_MODEL_ORDER if m in row_map]


def scenario_sort_key(scenario_id: str) -> tuple[int, str]:
    try:
        return (int(scenario_id[1:]), scenario_id)
    except ValueError:
        return (10**9, scenario_id)


DESCRIPTION_LEAD_MAP = {
    "provide": "Provides",
    "define": "Defines",
    "translate": "Translates",
    "summarize": "Summarizes",
    "check": "Checks",
    "embed": "Embeds",
    "generate": "Generates",
    "moderate": "Moderates",
    "persist": "Persists",
    "archive": "Archives",
    "transcribe": "Transcribes",
    "extract": "Extracts",
    "run": "Runs",
}


def normalize_task_description(description: str, *, component_group: str | None = None, role: str | None = None) -> str:
    if component_group == "aligned_context":
        if role and role.endswith("_client"):
            return "Provides local client configuration and shared helper utilities"
        if role and role.endswith("_models"):
            return "Defines local request/response models and normalization helpers"
        return "Provides local workflow scaffolding and helper utilities"

    text = " ".join(description.strip().split())
    text = text.rstrip(".")
    if not text:
        return text

    parts = text.split(" ", 1)
    first = parts[0]
    rest = parts[1] if len(parts) > 1 else ""
    mapped = DESCRIPTION_LEAD_MAP.get(first.lower())
    if mapped:
        return mapped if not rest else f"{mapped} {rest}"

    return text[0].upper() + text[1:]


def render_tasks_table(direct_tasks: list[dict], agentic_tasks: list[dict]) -> str:
    direct_map = {row["scenario_id"]: row for row in direct_tasks}
    agentic_map = {row["primary_atomic_scenario"]: row for row in agentic_tasks}
    scenario_ids = sorted(set(direct_map) & set(agentic_map), key=scenario_sort_key)

    lines = [
        r"\begingroup",
        r"\scriptsize",
        r"\setlength{\tabcolsep}{2pt}",
        r"\renewcommand{\arraystretch}{1.10}",
        r"\setlength{\LTleft}{0pt}",
        r"\setlength{\LTright}{0pt}",
        r"\begin{longtable}{>{\raggedright\arraybackslash}p{0.75cm} >{\raggedright\arraybackslash}p{2.45cm} >{\centering\arraybackslash}p{0.85cm} >{\centering\arraybackslash}p{1.00cm} >{\raggedright\arraybackslash}p{8.70cm}}",
        r"\caption{VIBench task catalog. Direct subtasks $T1$--$T4$ align with agentic core files $A1$--$A4$. $C1$--$C2$ denote local context/helper files and $I1$--$I4$ denote downstream agentic files.}",
        r"\label{tab:appendix-vibench-tasks}\\",
        r"\toprule",
        r"\textbf{ID} & \textbf{Scenario} & \textbf{Direct} & \textbf{Agentic} & \textbf{Description} \\",
        r"\midrule",
        r"\endfirsthead",
        r"\multicolumn{5}{l}{\textit{Table \thetable\ continued from previous page}}\\",
        r"\toprule",
        r"\textbf{ID} & \textbf{Scenario} & \textbf{Direct} & \textbf{Agentic} & \textbf{Description} \\",
        r"\midrule",
        r"\endhead",
        r"\midrule",
        r"\multicolumn{5}{r}{\textit{Continued on next page}}\\",
        r"\endfoot",
        r"\bottomrule",
        r"\endlastfoot",
    ]

    for scenario_idx, scenario_id in enumerate(scenario_ids):
        direct_row = direct_map[scenario_id]
        agentic_row = agentic_map[scenario_id]

        subtasks = sorted(direct_row["subtasks"], key=lambda row: row["index"])
        components = agentic_row["components"]
        aligned_core = sorted(
            [c for c in components if c["component_group"] == "aligned_core"],
            key=lambda c: c.get("atomic_subtask_index", 10**9),
        )
        aligned_context = [c for c in components if c["component_group"] == "aligned_context"]
        downstream = [c for c in components if c["component_group"] == "downstream"]

        title = escape_latex(direct_row["title"])

        for idx, (subtask, component) in enumerate(zip(subtasks, aligned_core), start=1):
            sid_cell = escape_latex(scenario_id) if idx == 1 else ""
            title_cell = title if idx == 1 else ""
            lines.append(
                " & ".join(
                    [
                        sid_cell,
                        title_cell,
                        escape_latex(f"T{idx}"),
                        escape_latex(f"A{idx}"),
                        escape_latex(normalize_task_description(subtask["description"])),
                    ]
                )
                + r" \\"
            )

        lines.append(r"\cmidrule(lr){3-5}")
        for idx, component in enumerate(aligned_context, start=1):
            lines.append(
                " & ".join(
                    [
                        "",
                        "",
                        "",
                        escape_latex(f"C{idx}"),
                        escape_latex(
                            normalize_task_description(
                                component["description"],
                                component_group=component["component_group"],
                                role=component.get("role"),
                            )
                        ),
                    ]
                )
                + r" \\"
            )

        lines.append(r"\cmidrule(lr){3-5}")
        for idx, component in enumerate(downstream, start=1):
            lines.append(
                " & ".join(
                    [
                        "",
                        "",
                        "",
                        escape_latex(f"I{idx}"),
                        escape_latex(
                            normalize_task_description(
                                component["description"],
                                component_group=component["component_group"],
                                role=component.get("role"),
                            )
                        ),
                    ]
                )
                + r" \\"
            )

        if scenario_idx != len(scenario_ids) - 1:
            lines.append(r"\midrule")

    lines += [
        r"\end{longtable}",
        r"\endgroup",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate compact appendix tables from current_results.md.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--raw-out", required=True)
    parser.add_argument("--delta-out", required=False)
    parser.add_argument("--vib-out", required=True)
    parser.add_argument("--prompt-out", required=False)
    parser.add_argument("--tasks-out", required=False)
    parser.add_argument("--diagnostics-out", required=False)
    args = parser.parse_args()

    root_map = get_root_map(Path(args.input))

    direct_raw = {row["Model"]: row for row in root_table(root_map, "Direct Raw Ecosystem Rates")}
    agentic_raw = {row["Model"]: row for row in root_table(root_map, "Agentic Raw Summary")}
    direct_vib = {row["Model"]: row for row in root_table(root_map, "Direct VIB Significance")}
    agentic_vib = {row["Model"]: row for row in child_table(root_map, "Agentic VIB Significance", "All Variants: Aligned Core")}
    agentic_prompt_vib = {
        source_title: {row["Model"]: row for row in child_table(root_map, "Agentic VIB Significance", source_title)}
        for source_title, _label in AGENTIC_PROMPT_FORMATS
    }
    agentic_aligned_rates = compute_agentic_aligned_rates(AGENTIC_RESULTS_PATH)

    raw_rows = []
    for model_id in DIRECT_MODEL_ORDER:
        if model_id not in direct_raw:
            continue
        d = direct_raw[model_id]
        agt = agentic_aligned_rates.get(model_id, {})
        affil = d["Affil"]
        raw_rows.append({
            "model_id": model_id,
            "provider": provider_key(affil),
            "aws": d["AWS"],
            "google": d["Google"],
            "msoai": d["MS/OpenAI"],
            "ibm": d["IBM"],
            "alibaba": d["Alibaba"],
            "indep": d["Indep"],
            "agt_aws": agt.get("agt_aws", "--"),
            "agt_google": agt.get("agt_google", "--"),
            "agt_msoai": agt.get("agt_msoai", "--"),
            "agt_ibm": agt.get("agt_ibm", "--"),
            "agt_alibaba": agt.get("agt_alibaba", "--"),
            "agt_indep": agt.get("agt_indep", "--"),
        })

    adjusted_rows = []
    for model_id in ADJUSTED_MODEL_ORDER:
        d = direct_vib.get(model_id)
        if not d:
            continue
        a = agentic_vib.get(model_id)
        adjusted_rows.append({
            "model_id": model_id,
            "provider": provider_key(d["Affil"]),
            "direct_vib": d["VIB"],
            "direct_ci": d["95% boot CI"],
            "direct_p": d["p"],
            "direct_q": d["q"],
            "agentic_vib": a["VIB"] if a else "--",
            "agentic_ci": a["95% boot CI"] if a else "--",
            "agentic_p": a["p"] if a else "--",
            "agentic_q": a["q"] if a else "--",
            "transition_delta": subtract_metric_strings(a["VIB"], d["VIB"]) if a else "--",
        })

    direct_prompt_values = compute_direct_prompt_vib_rows(direct_vib)
    prompt_rows = []
    for model_id in ADJUSTED_MODEL_ORDER:
        d = direct_vib.get(model_id)
        if not d:
            continue
        row = {
            "model_id": model_id,
            "provider": provider_key(d["Affil"]),
            "nli": direct_prompt_values.get(model_id, {}).get("nli", "--"),
            "nli_p": direct_prompt_values.get(model_id, {}).get("nli_p", "--"),
            "nli_q": direct_prompt_values.get(model_id, {}).get("nli_q", "--"),
            "fim": direct_prompt_values.get(model_id, {}).get("fim", "--"),
            "fim_p": direct_prompt_values.get(model_id, {}).get("fim_p", "--"),
            "fim_q": direct_prompt_values.get(model_id, {}).get("fim_q", "--"),
            "reference_open": direct_prompt_values.get(model_id, {}).get("reference_open", "--"),
            "reference_open_p": direct_prompt_values.get(model_id, {}).get("reference_open_p", "--"),
            "reference_open_q": direct_prompt_values.get(model_id, {}).get("reference_open_q", "--"),
            "free": "--",
            "free_p": "--",
            "free_q": "--",
            "informed": "--",
            "informed_p": "--",
            "informed_q": "--",
        }
        free = agentic_prompt_vib["Free: Aligned Core"].get(model_id)
        informed = agentic_prompt_vib["Informed: Aligned Core"].get(model_id)
        if free:
            row["free"] = free["VIB"]
            row["free_p"] = format_pq(free["p"])
            row["free_q"] = format_pq(free["q"])
        if informed:
            row["informed"] = informed["VIB"]
            row["informed_p"] = format_pq(informed["p"])
            row["informed_q"] = format_pq(informed["q"])
        prompt_rows.append(row)

    raw_rows = direct_ordered_rows(raw_rows)
    adjusted_rows = adjusted_ordered_rows(adjusted_rows)
    prompt_rows = adjusted_ordered_rows(prompt_rows)

    raw_out = Path(args.raw_out)
    vib_out = Path(args.vib_out)
    raw_out.parent.mkdir(parents=True, exist_ok=True)
    vib_out.parent.mkdir(parents=True, exist_ok=True)
    raw_out.write_text(render_raw_table(raw_rows))
    vib_out.write_text(render_results_table(adjusted_rows))
    if args.prompt_out:
        prompt_out = Path(args.prompt_out)
        prompt_out.parent.mkdir(parents=True, exist_ok=True)
        prompt_out.write_text(render_prompt_format_table(prompt_rows))
    if args.delta_out:
        delta_out = Path(args.delta_out)
        delta_out.parent.mkdir(parents=True, exist_ok=True)
        delta_out.write_text("% Control-subtracted ecosystem table intentionally omitted from the appendix.\n")
    if args.tasks_out:
        tasks_out = Path(args.tasks_out)
        tasks_out.parent.mkdir(parents=True, exist_ok=True)
        tasks_out.write_text(
            render_tasks_table(
                load_jsonl(DIRECT_TASKS_PATH),
                load_jsonl(AGENTIC_TASKS_PATH),
            )
        )

    if args.diagnostics_out:
        diagnostics_out = Path(args.diagnostics_out)
        diagnostics_out.parent.mkdir(parents=True, exist_ok=True)
        diagnostics_out.write_text("% Diagnostic appendix tables intentionally omitted.\n")


if __name__ == "__main__":
    main()
