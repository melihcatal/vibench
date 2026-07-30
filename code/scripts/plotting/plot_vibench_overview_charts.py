#!/usr/bin/env python3
"""Generate a compact paper-facing SVG figure set for VIBench."""

from __future__ import annotations

import argparse
import math
import sys
from collections import Counter
from html import escape
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
EVAL_DIR = SCRIPT_DIR.parent / "evaluation"
if str(EVAL_DIR) not in sys.path:
    sys.path.insert(0, str(EVAL_DIR))

import evaluate as direct_eval  # noqa: E402
import evaluate_agentic as agentic_eval  # noqa: E402
import generate_vibench_results_markdown as reportlib  # noqa: E402


STRICT_CONTROLS = reportlib.STRICT_CONTROL_IDS
RAW_ECOSYSTEMS = [
    "aws",
    "google",
    "microsoft_openai",
    "ibm",
    "alibaba",
    "independent",
    "anthropic",
    "unknown",
]

MODEL_DISPLAY_NAMES = {
    "claude-sonnet-4.6": "Claude Sonnet 4.6",
    "deepseek-v3.2": "DeepSeek V3.2",
    "gemini-2.5-flash": "Gemini 2.5 Flash",
    "gemini-2.5-pro": "Gemini 2.5 Pro",
    "gpt-5.4": "GPT-5.4",
    "gpt-5.4-mini": "GPT-5.4 Mini",
    "granite-4.0-h-small": "Granite 4.0 H Small",
    "granite-4.0-h-tiny-local": "Granite 4.0 H Tiny (Local)",
    "grok-4-1-fast-reasoning": "Grok 4.1 Fast Reasoning",
    "mistral-large-3": "Mistral Large 3",
    "nova-2-lite": "Nova 2 Lite",
    "nova-pro": "Nova Pro",
    "qwen3-coder-flash": "Qwen3 Coder Flash",
    "qwen3.6-plus": "Qwen 3.6 Plus",
}

ECOSYSTEM_DISPLAY = {
    "aws": "AWS",
    "google": "Google",
    "microsoft_openai": "MS/OpenAI",
    "ibm": "IBM",
    "alibaba": "Alibaba",
    "independent": "Independent",
    "anthropic": "Anthropic",
    "unknown": "Unknown",
}

ROLE_RANK = {"affiliated": 0, "control": 1, "independent": 2}

PALETTE = {
    "aws": "#FF9900",
    "google": "#4285F4",
    "microsoft_openai": "#0078D4",
    "ibm": "#0F62FE",
    "alibaba": "#FF6A00",
    "anthropic": "#A15C38",
    "independent": "#5F6368",
    "unknown": "#D0D7DE",
}

NEUTRAL = {
    "bg": "#FFFFFF",
    "text": "#202124",
    "muted": "#5F6368",
    "grid": "#E8EAED",
    "panel": "#F8F9FA",
    "border": "#DADCE0",
}

TRANSITION_COLORS = {
    "free": "#2563EB",
    "informed": "#0F766E",
    "negative": "#C2410C",
}


class SvgCanvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.elements: list[str] = []

    def rect(self, x, y, width, height, fill, stroke="none", stroke_width=0, rx=0):
        self.elements.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" rx="{rx}"/>'
        )

    def line(self, x1, y1, x2, y2, stroke, stroke_width=1, dash=None):
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        self.elements.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{stroke_width}"{dash_attr}/>'
        )

    def text(self, x, y, text, *, size=12, fill=None, anchor="start", weight="normal"):
        fill = fill or NEUTRAL["text"]
        self.elements.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
            f'font-family="Helvetica, Arial, sans-serif" text-anchor="{anchor}" '
            f'font-weight="{weight}">{escape(str(text))}</text>'
        )

    def save(self, path: Path):
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
            f'viewBox="0 0 {self.width} {self.height}">\n'
            f'  <rect width="{self.width}" height="{self.height}" fill="{NEUTRAL["bg"]}"/>\n'
            f'  ' + "\n  ".join(self.elements) + "\n</svg>\n"
        )
        path.write_text(svg, encoding="utf-8")


def display_model(model_id: str) -> str:
    return MODEL_DISPLAY_NAMES.get(model_id, model_id.replace("-", " "))


def role_order(model_id: str, models_info: dict) -> tuple[int, str]:
    role = models_info.get(model_id, {}).get("role")
    return ROLE_RANK.get(role, 9), display_model(model_id)


def significance_marker(row: dict | None) -> str:
    if not row:
        return ""
    value = row.get("q_value")
    if value is None:
        value = row.get("p_value")
    if value is None:
        return ""
    if value < 0.05:
        return "*"
    return ""


def hex_to_rgb(value: str):
    value = value.lstrip("#")
    return tuple(int(value[idx:idx + 2], 16) for idx in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb


def blend(color_a: str, color_b: str, t: float):
    rgb_a = hex_to_rgb(color_a)
    rgb_b = hex_to_rgb(color_b)
    return rgb_to_hex(tuple(int(round(a + (b - a) * t)) for a, b in zip(rgb_a, rgb_b)))


def sequential_fill(value: float | None, vmax: float):
    if value is None or value != value:
        return "#F3F4F6"
    ratio = min(max(value, 0.0) / max(vmax, 1e-9), 1.0)
    return blend("#FFFFFF", "#0F766E", ratio)


def diverging_fill(value: float | None, vmax: float):
    if value is None or value != value:
        return "#F3F4F6"
    ratio = min(abs(value) / max(vmax, 1e-9), 1.0)
    if value >= 0:
        return blend("#FFFFFF", "#B91C1C", ratio)
    return blend("#FFFFFF", "#1D4ED8", ratio)


def make_x_scale(x_min, x_max, left, right):
    span = max(x_max - x_min, 1e-9)

    def scale(value):
        return left + ((value - x_min) / span) * (right - left)

    return scale


def build_agentic_aligned_raw_rows(agentic_results, models_info):
    stats = agentic_eval.build_agentic_stats(agentic_results, "aligned_core")
    rows = []
    for model_id in sorted(stats, key=lambda mid: role_order(mid, models_info)):
        total = 0
        counts = Counter()
        for bucket in stats[model_id].values():
            total += bucket["total"]
            counts.update(bucket["counts"])
        if total <= 0:
            continue
        known_mass = sum(counts.values())
        row = {
            "model_id": model_id,
            "role": models_info.get(model_id, {}).get("role"),
            "affiliation": models_info.get(model_id, {}).get("ecosystem_affiliation")
            or models_info.get(model_id, {}).get("cloud_affiliation"),
        }
        for ecosystem in RAW_ECOSYSTEMS:
            if ecosystem == "unknown":
                row[ecosystem] = max(0.0, total - known_mass) / total
            else:
                row[ecosystem] = counts.get(ecosystem, 0.0) / total
        rows.append(row)
    return rows


def build_direct_condition_rows(direct_records, models_info):
    conditions = {
        "Direct NLI": ("nli",),
        "Direct FIM": ("fim",),
        "Direct Reference": (direct_eval.OPEN_REFERENCE_MODALITY, direct_eval.LEGACY_CS_MODALITY),
    }
    rows = {}
    for label, modalities in conditions.items():
        stats = agentic_eval.build_direct_stats(direct_records, "aligned_core", modalities)
        vib = agentic_eval.compute_matched_vib(stats, models_info, STRICT_CONTROLS)
        rows[label] = reportlib.matched_vib_significance_rows(
            stats,
            models_info,
            vib,
            bootstrap_source={"kind": "direct", "records": direct_records, "modalities": modalities, "level": "aligned_core"},
        )
    return rows


def build_agentic_condition_rows(agentic_results, models_info):
    rows = {}
    for label, variant in (("Agentic Free", "free"), ("Agentic Informed", "informed")):
        stats = agentic_eval.build_agentic_stats(agentic_results, "aligned_core", variant=variant)
        vib = agentic_eval.compute_matched_vib(stats, models_info, STRICT_CONTROLS)
        rows[label] = reportlib.matched_vib_significance_rows(
            stats,
            models_info,
            vib,
            bootstrap_source={"kind": "agentic", "results": agentic_results, "level": "aligned_core", "variant": variant},
        )
    return rows


def diff_in_diff_stats(model_a, total_a, ctrl_a, ctrl_total_a, model_b, total_b, ctrl_b, ctrl_total_b):
    if min(total_a, ctrl_total_a, total_b, ctrl_total_b) <= 0:
        return {"delta": None, "ci": None, "p_value": None}
    rate_model_a = model_a / total_a
    rate_ctrl_a = ctrl_a / ctrl_total_a
    rate_model_b = model_b / total_b
    rate_ctrl_b = ctrl_b / ctrl_total_b
    delta = (rate_model_a - rate_ctrl_a) - (rate_model_b - rate_ctrl_b)
    se = math.sqrt(
        (rate_model_a * (1 - rate_model_a) / total_a) +
        (rate_ctrl_a * (1 - rate_ctrl_a) / ctrl_total_a) +
        (rate_model_b * (1 - rate_model_b) / total_b) +
        (rate_ctrl_b * (1 - rate_ctrl_b) / ctrl_total_b)
    )
    if se == 0:
        p_value = 0.0 if delta != 0 else 1.0
        ci = (delta, delta)
    else:
        z = delta / se
        p_value = 2 * (1 - reportlib.normal_cdf(abs(z)))
        ci = (delta - 1.96 * se, delta + 1.96 * se)
    return {"delta": delta, "ci": ci, "p_value": p_value}


def build_transition_rows(direct_records, agentic_results, models_info):
    rows = {}
    specs = {
        "Free vs NLI": {
            "direct_stats": agentic_eval.build_direct_stats(direct_records, "aligned_core", ("nli",)),
            "agentic_stats": agentic_eval.build_agentic_stats(agentic_results, "aligned_core", variant="free"),
        },
        "Informed vs Reference": {
            "direct_stats": agentic_eval.build_direct_stats(
                direct_records,
                "aligned_core",
                (direct_eval.OPEN_REFERENCE_MODALITY, direct_eval.LEGACY_CS_MODALITY),
            ),
            "agentic_stats": agentic_eval.build_agentic_stats(agentic_results, "aligned_core", variant="informed"),
        },
    }
    for label, spec in specs.items():
        agentic_vib = agentic_eval.compute_matched_vib(spec["agentic_stats"], models_info, STRICT_CONTROLS)
        table = reportlib.transition_rows(
            spec["direct_stats"],
            spec["agentic_stats"],
            models_info,
            label,
            agentic_vib,
            direct_bootstrap_source={
                "records": direct_records,
                "modalities": ("nli",) if label == "Free vs NLI" else (direct_eval.OPEN_REFERENCE_MODALITY, direct_eval.LEGACY_CS_MODALITY),
                "level": "aligned_core",
            },
            agentic_bootstrap_source={
                "results": agentic_results,
                "variant": "free" if label == "Free vs NLI" else "informed",
                "level": "aligned_core",
            },
        )
        table.sort(key=lambda row: (row["delta_vib"] is None, -(abs(row["delta_vib"] or 0.0)), display_model(row["model_id"])))
        rows[label] = table
    return rows


def build_data(direct_run: Path, agentic_run: Path):
    models_info = direct_eval.load_models("vibench")
    direct_records = direct_eval.load_labeled_outputs(direct_run)
    agentic_results = reportlib.load_agentic_results(agentic_run)

    direct_raw_rows, _, _, _ = reportlib.direct_raw_rows(direct_records, models_info)
    direct_conditions = build_direct_condition_rows(direct_records, models_info)
    agentic_conditions = build_agentic_condition_rows(agentic_results, models_info)

    return {
        "models_info": models_info,
        "direct_raw_rows": direct_raw_rows,
        "agentic_raw_rows": build_agentic_aligned_raw_rows(agentic_results, models_info),
        "modality_tables": {**direct_conditions, **agentic_conditions},
        "transition_tables": build_transition_rows(direct_records, agentic_results, models_info),
    }


def draw_raw_heatmap(rows, models_info, title, out_path: Path):
    ordered = sorted((row for row in rows), key=lambda row: role_order(row["model_id"], models_info))
    row_label_w = 265
    cell_w = 112
    cell_h = 34
    width = row_label_w + len(RAW_ECOSYSTEMS) * cell_w + 44
    height = 110 + len(ordered) * cell_h + 28
    vmax = 80.0
    canvas = SvgCanvas(width, height)
    canvas.text(width / 2, 34, title, size=24, anchor="middle", weight="bold")

    grid_x = row_label_w
    grid_y = 74
    for col_idx, ecosystem in enumerate(RAW_ECOSYSTEMS):
        cx = grid_x + col_idx * cell_w + cell_w / 2
        canvas.text(cx, 62, ECOSYSTEM_DISPLAY[ecosystem], size=12, anchor="middle", weight="bold")

    prev_role = None
    for row_idx, row in enumerate(ordered):
        y = grid_y + row_idx * cell_h
        role = models_info.get(row["model_id"], {}).get("role")
        if prev_role is not None and role != prev_role:
            canvas.line(22, y - 6, width - 22, y - 6, NEUTRAL["border"], stroke_width=2)
        prev_role = role
        canvas.text(grid_x - 14, y + 22, display_model(row["model_id"]), size=13, anchor="end", weight="bold")
        for col_idx, ecosystem in enumerate(RAW_ECOSYSTEMS):
            value = (row.get(ecosystem) or 0.0) * 100
            x = grid_x + col_idx * cell_w
            fill = sequential_fill(value, vmax)
            border = "none"
            border_width = 0
            affiliation = row.get("affiliation")
            if affiliation and affiliation == ecosystem:
                border = "#111827"
                border_width = 2
            canvas.rect(x, y, cell_w - 2, cell_h - 2, fill, stroke=border, stroke_width=border_width, rx=5)
            text_fill = "#FFFFFF" if value >= 45 else NEUTRAL["text"]
            canvas.text(x + cell_w / 2 - 1, y + 22, f"{value:.1f}", size=11, anchor="middle", fill=text_fill, weight="bold")
    canvas.save(out_path)


def draw_modality_heatmap(modality_tables, models_info, out_path: Path):
    condition_order = [
        "Direct NLI",
        "Direct FIM",
        "Direct Reference",
        "Agentic Free",
        "Agentic Informed",
    ]
    maps = {label: reportlib.vib_row_map(modality_tables[label]) for label in condition_order}
    model_ids = sorted(
        set().union(*(mapping.keys() for mapping in maps.values())),
        key=lambda model_id: (
            -max(abs((maps[label].get(model_id, {}).get("vib") or 0.0) * 100) for label in condition_order),
            display_model(model_id),
        ),
    )
    row_label_w = 265
    cell_w = 146
    cell_h = 48
    width = row_label_w + len(condition_order) * cell_w + 44
    height = 118 + len(model_ids) * cell_h + 24
    vmax = 40.0
    canvas = SvgCanvas(width, height)
    canvas.text(width / 2, 34, "VIB by Prompt Condition", size=24, anchor="middle", weight="bold")

    grid_x = row_label_w
    grid_y = 82
    for col_idx, label in enumerate(condition_order):
        cx = grid_x + col_idx * cell_w + cell_w / 2
        canvas.text(cx, 68, label, size=12, anchor="middle", weight="bold")

    for row_idx, model_id in enumerate(model_ids):
        y = grid_y + row_idx * cell_h
        canvas.text(grid_x - 14, y + 29, display_model(model_id), size=13, anchor="end", weight="bold")
        for col_idx, label in enumerate(condition_order):
            row = maps[label].get(model_id)
            value = (row.get("vib") or 0.0) * 100 if row else None
            x = grid_x + col_idx * cell_w
            fill = diverging_fill(value, vmax)
            canvas.rect(x, y, cell_w - 2, cell_h - 2, fill, stroke="#FFFFFF", stroke_width=1, rx=5)
            if row and value is not None:
                text_fill = "#FFFFFF" if abs(value) >= 18 else NEUTRAL["text"]
                canvas.text(x + cell_w / 2, y + 24, f"{value:+.1f}", size=12, anchor="middle", fill=text_fill, weight="bold")
                stars = significance_marker(row)
                if stars:
                    canvas.text(x + cell_w / 2, y + 40, stars, size=11, anchor="middle", fill=text_fill, weight="bold")
            else:
                canvas.text(x + cell_w / 2, y + 29, "n/a", size=12, anchor="middle", fill=NEUTRAL["muted"])
    canvas.save(out_path)


def draw_transition_chart(transition_tables, models_info, out_path: Path):
    free_map = {row["model_id"]: row for row in transition_tables["Free vs NLI"]}
    informed_map = {row["model_id"]: row for row in transition_tables["Informed vs Reference"]}
    model_ids = sorted(
        set(free_map) | set(informed_map),
        key=lambda model_id: (
            -max(
                abs((free_map.get(model_id, {}).get("delta_vib") or 0.0) * 100),
                abs((informed_map.get(model_id, {}).get("delta_vib") or 0.0) * 100),
            ),
            display_model(model_id),
        ),
    )
    label_w = 260
    panel_w = 420
    panel_gap = 80
    left_plot = label_w + 40
    mid_plot = left_plot + panel_w
    right_plot = mid_plot + panel_gap
    far_right = right_plot + panel_w
    row_h = 52
    width = far_right + 32
    height = 126 + len(model_ids) * row_h + 34
    vmax = 40.0
    all_values = [
        abs((row.get("delta_vib") or 0.0) * 100)
        for row in transition_tables["Free vs NLI"] + transition_tables["Informed vs Reference"]
    ]
    if all_values:
        vmax = max(vmax, math.ceil(max(all_values) / 5.0) * 5.0)
    scale_left = make_x_scale(-vmax, vmax, left_plot, mid_plot)
    scale_right = make_x_scale(-vmax, vmax, right_plot, far_right)

    def draw_panel_header(scale, x1, x2, label):
        canvas.text((x1 + x2) / 2, 68, label, size=14, anchor="middle", weight="bold")
        zero = scale(0.0)
        canvas.line(zero, 84, zero, height - 36, "#9CA3AF", stroke_width=2)
        for tick in range(-int(vmax), int(vmax) + 1, 10):
            x = scale(tick)
            canvas.line(x, 84, x, height - 36, NEUTRAL["grid"], stroke_width=1)
            canvas.text(x, 98, f"{tick:+d}", size=10, anchor="middle", fill=NEUTRAL["muted"])

    canvas = SvgCanvas(width, height)
    canvas.text(width / 2, 34, "Direct to Agentic Transition in VIB", size=24, anchor="middle", weight="bold")
    draw_panel_header(scale_left, left_plot, mid_plot, "Free vs NLI")
    draw_panel_header(scale_right, right_plot, far_right, "Informed vs Reference")

    for row_idx, model_id in enumerate(model_ids):
        y = 126 + row_idx * row_h
        canvas.text(label_w, y + 7, display_model(model_id), size=13, anchor="end", weight="bold")
        for mapping, scale, color in (
            (free_map, scale_left, TRANSITION_COLORS["free"]),
            (informed_map, scale_right, TRANSITION_COLORS["informed"]),
        ):
            row = mapping.get(model_id)
            if not row:
                continue
            value = (row.get("delta_vib") or 0.0) * 100
            start = scale(0.0)
            end = scale(value)
            fill = color if value >= 0 else TRANSITION_COLORS["negative"]
            canvas.rect(min(start, end), y - 10, max(2.0, abs(end - start)), 20, fill, rx=4)
            stars = significance_marker(row)
            label = f"{value:+.1f}{stars}"
            anchor = "start" if value >= 0 else "end"
            lx = end + 10 if value >= 0 else end - 10
            canvas.text(lx, y + 5, label, size=12, anchor=anchor, weight="bold")
    canvas.save(out_path)


def main():
    parser = argparse.ArgumentParser(description="Generate the current VIBench SVG figure set.")
    parser.add_argument("--direct-run", required=True, help="Direct run directory or identifier")
    parser.add_argument("--agentic-run", required=True, help="Agentic run directory or identifier")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    args = parser.parse_args()

    direct_run = direct_eval.resolve_run_dir(args.direct_run)
    if direct_run is None:
        raise SystemExit(f"Could not resolve direct run: {args.direct_run}")
    agentic_run = direct_eval.resolve_run_dir(args.agentic_run)
    if agentic_run is None:
        raise SystemExit(f"Could not resolve agentic run: {args.agentic_run}")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    data = build_data(direct_run, agentic_run)

    draw_raw_heatmap(
        data["direct_raw_rows"],
        data["models_info"],
        "Raw Direct Ecosystem Rates",
        out_dir / "vibench_raw_direct_heatmap.svg",
    )
    draw_raw_heatmap(
        data["agentic_raw_rows"],
        data["models_info"],
        "Raw Agentic Ecosystem Rates",
        out_dir / "vibench_raw_agentic_heatmap.svg",
    )
    draw_modality_heatmap(
        data["modality_tables"],
        data["models_info"],
        out_dir / "vibench_modality_comparison.svg",
    )
    draw_transition_chart(
        data["transition_tables"],
        data["models_info"],
        out_dir / "vibench_transition_comparison.svg",
    )

    for name in (
        "vibench_raw_direct_heatmap.svg",
        "vibench_raw_agentic_heatmap.svg",
        "vibench_modality_comparison.svg",
        "vibench_transition_comparison.svg",
    ):
        print(out_dir / name)


if __name__ == "__main__":
    main()
