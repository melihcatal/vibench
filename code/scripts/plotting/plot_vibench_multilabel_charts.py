#!/usr/bin/env python3
"""Render VIBench legacy-single vs share-normalized sensitivity charts as SVG."""

from __future__ import annotations

import argparse
import json
import sys
from html import escape
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
EVAL_DIR = SCRIPT_DIR.parent / "evaluation"
# The evaluation modules form one namespace, grouped into folders for readability.
for _group in ("core", "gini", "tables", "baselines", "audit"):
    if str(EVAL_DIR / _group) not in sys.path:
        sys.path.insert(0, str(EVAL_DIR / _group))

import evaluate as direct_eval  # noqa: E402
import model_registry as registry  # noqa: E402
import evaluate_agentic as agentic_eval  # noqa: E402
import generate_vibench_results_markdown as results_md  # noqa: E402


STRICT_CONTROL_IDS = registry.strict_controls()

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

PALETTE = {
    "aws": "#FF9900",
    "google": "#4285F4",
    "microsoft_openai": "#2B6CB0",
    "ibm": "#0F62FE",
    "alibaba": "#FF6A00",
}

NEUTRAL_COLORS = {
    "axis": "#202124",
    "grid": "#E8EAED",
    "text": "#202124",
    "muted": "#5F6368",
    "bg": "#FFFFFF",
    "panel": "#F8F9FA",
    "bar_light": "#B0BEC5",
    "bar_mid": "#78909C",
    "bar_dark": "#455A64",
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

    def line(self, x1, y1, x2, y2, stroke, stroke_width=1, dash=None, opacity=1.0):
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        self.elements.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{stroke_width}" opacity="{opacity:.3f}"{dash_attr}/>'
        )

    def circle(self, cx, cy, r, fill, stroke="none", stroke_width=0):
        self.elements.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{stroke_width}"/>'
        )

    def text(self, x, y, text, size=12, fill=None, anchor="start", weight="normal"):
        fill = fill or NEUTRAL_COLORS["text"]
        safe = escape(str(text))
        self.elements.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
            f'font-family="Helvetica, Arial, sans-serif" text-anchor="{anchor}" '
            f'font-weight="{weight}">{safe}</text>'
        )

    def to_svg(self) -> str:
        body = "\n  ".join(self.elements)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
            f'viewBox="0 0 {self.width} {self.height}">\n'
            f'  <rect width="{self.width}" height="{self.height}" fill="{NEUTRAL_COLORS["bg"]}"/>\n'
            f'  {body}\n'
            f"</svg>\n"
        )

    def save(self, path: Path):
        path.write_text(self.to_svg(), encoding="utf-8")


def affiliation_rows(models_info):
    rows = []
    for model_id, info in models_info.items():
        if info.get("role") != "affiliated":
            continue
        affiliation = info.get("ecosystem_affiliation") or info.get("cloud_affiliation")
        if affiliation:
            rows.append((model_id, affiliation))
    return rows


def display_model(model_id: str) -> str:
    return MODEL_DISPLAY_NAMES.get(model_id) or registry.display_name(model_id)


def load_agentic_results(run_dir: Path):
    with open(run_dir / "labeled" / "agentic" / "results.json") as f:
        return json.load(f)


def direct_single_multi(models_info, direct_records):
    _, counts_share, totals_share = direct_eval.compute_frr(direct_records, field="detected_ecosystem", mode="share")
    share_rows = results_md.direct_vib_rows(models_info, counts_share, totals_share)
    _, counts_single, totals_single = direct_eval.compute_frr(direct_records, field="detected_ecosystem", mode="single")
    single_rows = results_md.direct_vib_rows(models_info, counts_single, totals_single)
    return results_md.build_direct_multilabel_summary_rows(
        direct_records,
        models_info,
        single_rows,
        share_rows,
    )


def agentic_single_multi(models_info, agentic_results):
    primary_single_stats = agentic_eval.build_agentic_stats(agentic_results, "primary", mode="single")
    aligned_single_stats = agentic_eval.build_agentic_stats(agentic_results, "aligned_core", mode="single")
    primary_multi_stats = agentic_eval.build_agentic_stats(agentic_results, "primary", mode="share")
    aligned_multi_stats = agentic_eval.build_agentic_stats(agentic_results, "aligned_core", mode="share")

    primary_single = results_md.matched_vib_significance_rows(
        primary_single_stats,
        models_info,
        agentic_eval.compute_matched_vib(primary_single_stats, models_info, STRICT_CONTROL_IDS),
    )
    aligned_single = results_md.matched_vib_significance_rows(
        aligned_single_stats,
        models_info,
        agentic_eval.compute_matched_vib(aligned_single_stats, models_info, STRICT_CONTROL_IDS),
    )
    primary_multi = results_md.matched_vib_significance_rows(
        primary_multi_stats,
        models_info,
        agentic_eval.compute_matched_vib(primary_multi_stats, models_info, STRICT_CONTROL_IDS),
    )
    aligned_multi = results_md.matched_vib_significance_rows(
        aligned_multi_stats,
        models_info,
        agentic_eval.compute_matched_vib(aligned_multi_stats, models_info, STRICT_CONTROL_IDS),
    )

    return results_md.build_agentic_multilabel_summary_rows(
        agentic_results,
        models_info,
        primary_single,
        primary_multi,
        aligned_single,
        aligned_multi,
    )


def value_range(values, pad=2.0):
    values = [value for value in values if value is not None]
    if not values:
        return -10.0, 10.0
    low = min(values)
    high = max(values)
    low = min(low, 0.0)
    high = max(high, 0.0)
    if abs(high - low) < 1e-9:
        low -= 1.0
        high += 1.0
    return low - pad, high + pad


def make_x_scale(x_min, x_max, left, right):
    span = max(x_max - x_min, 1e-9)

    def scale(value):
        return left + ((value - x_min) / span) * (right - left)

    return scale


def draw_x_axis(canvas: SvgCanvas, x_min, x_max, scale, top, bottom, ticks=6):
    if x_min >= 0:
        zero = scale(x_min)
    elif x_max <= 0:
        zero = scale(x_max)
    else:
        zero = scale(0.0)
    canvas.line(zero, top, zero, bottom, NEUTRAL_COLORS["axis"], stroke_width=1.5)
    step = (x_max - x_min) / ticks
    for idx in range(ticks + 1):
        value = x_min + idx * step
        x = scale(value)
        canvas.line(x, top, x, bottom, NEUTRAL_COLORS["grid"], stroke_width=1)
        canvas.text(x, bottom + 18, f"{value:+.0f}", size=11, fill=NEUTRAL_COLORS["muted"], anchor="middle")


def plot_direct_single_vs_multi(rows, out_dir: Path):
    rows = [row for row in rows if row["primary_vib"] is not None and row["multi_vib"] is not None]
    rows.sort(key=lambda row: row["multi_vib"], reverse=True)

    width = 1100
    row_gap = 54
    top = 92
    bottom_pad = 70
    left = 330
    right = width - 120
    height = top + len(rows) * row_gap + bottom_pad

    values = [(row["primary_vib"] or 0.0) * 100 for row in rows] + [(row["multi_vib"] or 0.0) * 100 for row in rows]
    x_min, x_max = value_range(values, pad=3.0)
    scale = make_x_scale(x_min, x_max, left, right)

    canvas = SvgCanvas(width, height)
    canvas.text(width / 2, 34, "Direct VIB: Legacy First-Label vs Share-Normalized", size=22, anchor="middle", weight="bold")
    canvas.text(width / 2, 58, "Sensitivity check: each file contributes total mass 1 split across detected ecosystems", size=13, fill=NEUTRAL_COLORS["muted"], anchor="middle")

    draw_x_axis(canvas, x_min, x_max, scale, top, height - bottom_pad, ticks=7)

    for idx, row in enumerate(rows):
        y = top + idx * row_gap + 16
        color = PALETTE.get(row["affiliation"], NEUTRAL_COLORS["muted"])
        primary = (row["primary_vib"] or 0.0) * 100
        multi = (row["multi_vib"] or 0.0) * 100
        canvas.text(left - 16, y + 4, display_model(row["model_id"]), size=13, anchor="end")
        canvas.line(scale(primary), y, scale(multi), y, color, stroke_width=3, opacity=0.85)
        canvas.circle(scale(primary), y, 6, "white", stroke=color, stroke_width=2.5)
        canvas.circle(scale(multi), y, 7, color, stroke="white", stroke_width=1.5)
        canvas.text(scale(multi) + 12, y + 4, f"{row['delta_vib'] * 100:+.1f}pp", size=11, fill=color)

    legend_y = height - 28
    canvas.circle(325, legend_y - 4, 6, "white", stroke="#5F6368", stroke_width=2)
    canvas.text(340, legend_y, "Primary-label VIB", size=12)
    canvas.circle(485, legend_y - 4, 7, "#5F6368", stroke="white", stroke_width=1)
    canvas.text(500, legend_y, "Multi-provider incidence VIB", size=12)
    canvas.save(out_dir / "vibench_direct_single_vs_multi_vib.svg")


def draw_lollipop_panel(canvas: SvgCanvas, panel_x, panel_y, panel_w, panel_h, rows, title, left_key, right_key, delta_key):
    header_h = 36
    plot_top = panel_y + header_h + 12
    plot_bottom = panel_y + panel_h - 40
    label_left = panel_x + 12
    axis_left = panel_x + 240
    axis_right = panel_x + panel_w - 26

    values = [(row[left_key] or 0.0) * 100 for row in rows] + [(row[right_key] or 0.0) * 100 for row in rows]
    x_min, x_max = value_range(values, pad=3.0)
    scale = make_x_scale(x_min, x_max, axis_left, axis_right)

    canvas.rect(panel_x, panel_y, panel_w, panel_h, NEUTRAL_COLORS["panel"], stroke="#DADCE0", stroke_width=1, rx=10)
    canvas.text(panel_x + panel_w / 2, panel_y + 24, title, size=16, anchor="middle", weight="bold")
    draw_x_axis(canvas, x_min, x_max, scale, plot_top, plot_bottom, ticks=5)

    row_gap = (plot_bottom - plot_top) / max(len(rows), 1)
    for idx, row in enumerate(rows):
        y = plot_top + row_gap * idx + row_gap / 2
        color = PALETTE.get(row["affiliation"], NEUTRAL_COLORS["muted"])
        left_val = (row[left_key] or 0.0) * 100
        right_val = (row[right_key] or 0.0) * 100
        canvas.text(axis_left - 10, y + 4, display_model(row["model_id"]), size=12, anchor="end")
        canvas.line(scale(left_val), y, scale(right_val), y, color, stroke_width=3, opacity=0.85)
        canvas.circle(scale(left_val), y, 5.5, "white", stroke=color, stroke_width=2.2)
        canvas.circle(scale(right_val), y, 6.5, color, stroke="white", stroke_width=1.3)
        canvas.text(scale(right_val) + 10, y + 4, f"{row[delta_key] * 100:+.1f}pp", size=10, fill=color)


def plot_agentic_single_vs_multi(rows, out_dir: Path):
    rows = [row for row in rows if row["primary_vib"] is not None and row["primary_multi_vib"] is not None]
    rows.sort(key=lambda row: row["primary_multi_vib"], reverse=True)

    width = 1500
    height = 620
    canvas = SvgCanvas(width, height)
    canvas.text(width / 2, 34, "Agentic VIB: Legacy First-Label vs Share-Normalized", size=22, anchor="middle", weight="bold")
    canvas.text(width / 2, 58, "Matched-scenario VIB; dots show legacy first-label and share-normalized estimates", size=13, fill=NEUTRAL_COLORS["muted"], anchor="middle")

    panel_y = 82
    panel_h = 500
    gap = 28
    panel_w = (width - 48 - gap) / 2
    draw_lollipop_panel(canvas, 24, panel_y, panel_w, panel_h, rows, "Primary Anchor", "primary_vib", "primary_multi_vib", "primary_delta_vib")
    draw_lollipop_panel(canvas, 24 + panel_w + gap, panel_y, panel_w, panel_h, rows, "Aligned Core Files", "aligned_vib", "aligned_multi_vib", "aligned_delta_vib")

    legend_y = height - 18
    canvas.circle(width / 2 - 140, legend_y - 4, 5.5, "white", stroke="#5F6368", stroke_width=2)
    canvas.text(width / 2 - 124, legend_y, "Legacy first-label VIB", size=12)
    canvas.circle(width / 2 + 20, legend_y - 4, 6.5, "#5F6368", stroke="white", stroke_width=1)
    canvas.text(width / 2 + 36, legend_y, "Share-normalized VIB", size=12)
    canvas.save(out_dir / "vibench_agentic_single_vs_multi_vib.svg")


def plot_multi_provider_rates(direct_rows, agentic_rows, out_dir: Path):
    agentic_map = {row["model_id"]: row for row in agentic_rows}
    rows = []
    for row in direct_rows:
        if row["model_id"] not in agentic_map:
            continue
        primary_rate = agentic_map[row["model_id"]].get("primary_multi_provider_rate")
        component_rate = agentic_map[row["model_id"]].get("component_multi_provider_rate")
        direct_rate = row.get("multi_provider_rate")
        if primary_rate is None or component_rate is None or direct_rate is None:
            continue
        rows.append({
            "model_id": row["model_id"],
            "affiliation": row["affiliation"],
            "direct": direct_rate * 100,
            "agentic_primary": primary_rate * 100,
            "agentic_component": component_rate * 100,
        })
    rows.sort(key=lambda row: row["agentic_component"], reverse=True)

    width = 1200
    row_gap = 58
    top = 88
    bottom_pad = 70
    left = 340
    right = width - 120
    height = top + len(rows) * row_gap + bottom_pad
    x_min, x_max = value_range([0.0] + [row["agentic_component"] for row in rows], pad=1.0)
    scale = make_x_scale(0.0, x_max, left, right)

    canvas = SvgCanvas(width, height)
    canvas.text(width / 2, 34, "Multi-Provider Prevalence by Model", size=22, anchor="middle", weight="bold")
    canvas.text(width / 2, 58, "Direct files versus agentic primary files versus all scored agentic components", size=13, fill=NEUTRAL_COLORS["muted"], anchor="middle")
    draw_x_axis(canvas, 0.0, x_max, scale, top, height - bottom_pad, ticks=6)

    for idx, row in enumerate(rows):
        y_center = top + idx * row_gap + 18
        color = PALETTE.get(row["affiliation"], NEUTRAL_COLORS["muted"])
        canvas.text(left - 16, y_center + 5, display_model(row["model_id"]), size=13, anchor="end")
        for offset, key, fill in (
            (-12, "direct", NEUTRAL_COLORS["bar_light"]),
            (0, "agentic_primary", NEUTRAL_COLORS["bar_mid"]),
            (12, "agentic_component", color if color != NEUTRAL_COLORS["muted"] else NEUTRAL_COLORS["bar_dark"]),
        ):
            value = row[key]
            y = y_center + offset - 6
            canvas.rect(left, y, max(scale(value) - left, 0.0), 10, fill)
        canvas.text(scale(row["agentic_component"]) + 10, y_center + 5, f"{row['agentic_component']:.1f}%", size=11, fill=color)

    legend_y = height - 26
    legend_x = 320
    for fill, label in (
        (NEUTRAL_COLORS["bar_light"], "Direct file"),
        (NEUTRAL_COLORS["bar_mid"], "Agentic primary file"),
        (NEUTRAL_COLORS["bar_dark"], "Any scored agentic component"),
    ):
        canvas.rect(legend_x, legend_y - 10, 16, 10, fill)
        canvas.text(legend_x + 24, legend_y, label, size=12)
        legend_x += 195

    canvas.save(out_dir / "vibench_multi_provider_rates.svg")


def main():
    parser = argparse.ArgumentParser(description="Plot VIBench legacy-vs-share comparison charts.")
    parser.add_argument("--direct-run", required=True, help="Direct run directory or identifier")
    parser.add_argument("--agentic-run", required=True, help="Agentic run directory or identifier")
    parser.add_argument("--output-dir", required=True, help="Directory for output charts")
    args = parser.parse_args()

    direct_run = direct_eval.resolve_run_dir(args.direct_run)
    if direct_run is None:
        raise SystemExit(f"Could not resolve direct run: {args.direct_run}")
    agentic_run = direct_eval.resolve_run_dir(args.agentic_run)
    if agentic_run is None:
        raise SystemExit(f"Could not resolve agentic run: {args.agentic_run}")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    models_info = direct_eval.load_models("vibench")
    direct_records = direct_eval.load_labeled_outputs(direct_run)
    agentic_results = load_agentic_results(agentic_run)

    direct_rows = direct_single_multi(models_info, direct_records)
    agentic_rows = agentic_single_multi(models_info, agentic_results)

    plot_direct_single_vs_multi(direct_rows, out_dir)
    plot_agentic_single_vs_multi(agentic_rows, out_dir)
    plot_multi_provider_rates(direct_rows, agentic_rows, out_dir)
    print(out_dir)


if __name__ == "__main__":
    main()
