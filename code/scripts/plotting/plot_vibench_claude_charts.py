#!/usr/bin/env python3
"""Regenerate the high-resolution `claude_*` VIBench figure set."""

from __future__ import annotations

import argparse
import textwrap
import sys
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402


SCRIPT_DIR = Path(__file__).resolve().parent
EVAL_DIR = SCRIPT_DIR.parent / "evaluation"
if str(EVAL_DIR) not in sys.path:
    sys.path.insert(0, str(EVAL_DIR))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import evaluate as direct_eval  # noqa: E402
import evaluate_agentic as agentic_eval  # noqa: E402
import generate_vibench_results_markdown as reportlib  # noqa: E402
import model_registry as registry  # noqa: E402
import plot_vibench_overview_charts as overview  # noqa: E402


STRICT_CONTROLS = reportlib.STRICT_CONTROL_IDS

ECOSYSTEMS = [
    "aws",
    "google",
    "microsoft_openai",
    "ibm",
    "alibaba",
    "independent",
    "anthropic",
    "unknown",
]

ECOSYSTEM_LABEL = {
    "aws": "AWS",
    "google": "Google",
    "microsoft_openai": "MS/OpenAI",
    "ibm": "IBM",
    "alibaba": "Alibaba",
    "independent": "Independent",
    "anthropic": "Anthropic",
    "unknown": "Unknown",
}

MODEL_LABEL = {
    "claude-sonnet-4.6": "Claude Sonnet 4.6",
    "deepseek-v3.2": "DeepSeek V3.2",
    "gemini-2.5-flash": "Gemini 2.5 Flash",
    "gemini-2.5-pro": "Gemini 2.5 Pro",
    "gpt-5.4": "GPT-5.4",
    "gpt-5.4-mini": "GPT-5.4 Mini",
    "granite-4.0-h-small": "Granite 4.0 H Small",
    "granite-4.0-h-tiny-local": "Granite 4.0 H Tiny",
    "grok-4-1-fast-reasoning": "Grok 4.1 Fast",
    "mistral-large-3": "Mistral Large 3",
    "nova-2-lite": "Nova 2 Lite",
    "nova-pro": "Nova Pro",
    "qwen3-coder-flash": "Qwen3 Coder Flash",
    "qwen3.6-plus": "Qwen 3.6 Plus",
}

MODEL_LABEL_COMPACT = {
    "gemini-2.5-flash": "Gemini Flash",
    "gemini-2.5-pro": "Gemini Pro",
    "gpt-5.4": "GPT-5.4",
    "gpt-5.4-mini": "GPT-5.4 Mini",
    "granite-4.0-h-small": "Granite Small",
    "nova-pro": "Nova Pro",
    "qwen3.6-plus": "Qwen3.6 Plus",
}

ECOSYSTEM_LABEL_COMPACT = {
    "aws": "AWS",
    "google": "Google",
    "microsoft_openai": "MSFT/OAI",
    "ibm": "IBM",
    "alibaba": "Alibaba",
}

PALETTE = {
    "aws": "#ff9900",
    "google": "#4285f4",
    "microsoft_openai": "#2f80ed",
    "ibm": "#0f62fe",
    "alibaba": "#ff6a00",
    "independent": "#687385",
    "anthropic": "#a15c38",
    "unknown": "#b8c0cc",
}

ROLE_RANK = {"affiliated": 0, "control": 1, "independent": 2}
BG = "#ffffff"
PANEL = "#ffffff"
GRID = "#e5e7eb"
TEXT = "#0f172a"
MUTED = "#64748b"
SUBTLE = "#334155"

ECO_DIRECT = "#2563eb"    # blue - direct / neutral series
ECO_AGENTIC = "#e11d48"   # red  - agentic / affiliated / bias-positive
ECO_CONTROL = "#94a3b8"   # gray - control / baseline
ECO_SOFT_BLUE = "#dbeafe"
ECO_SOFT_RED = "#fee2e2"


def label_model(model_id: str) -> str:
    return MODEL_LABEL.get(model_id) or registry.display_name(model_id)


def label_model_compact(model_id: str) -> str:
    return MODEL_LABEL_COMPACT.get(model_id, label_model(model_id))


def role_sort(model_id: str, models_info: dict) -> tuple[int, str]:
    return ROLE_RANK.get(models_info.get(model_id, {}).get("role"), 9), label_model(model_id)


def affil(model_id: str, models_info: dict) -> str | None:
    info = models_info.get(model_id, {})
    return info.get("ecosystem_affiliation") or info.get("cloud_affiliation")


def ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def save(fig, path: Path) -> None:
    ensure_dir(path)
    # Honor the figure's own facecolor (important for charts that set pure white)
    fig.savefig(path, dpi=220, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(path)


def style_ax(ax, title: str, subtitle: str | None = None) -> None:
    ax.set_facecolor(PANEL)
    ax.set_title(title, loc="left", fontsize=14, fontweight="semibold", color=TEXT, pad=22)
    if subtitle:
        ax.text(0, 1.015, subtitle, transform=ax.transAxes, ha="left", va="bottom",
                fontsize=10.0, color=MUTED, style="italic")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=10, length=0)
    ax.grid(True, axis="x", color=GRID, linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    for lbl in ax.get_yticklabels():
        lbl.set_fontweight("semibold")
    for lbl in ax.get_xticklabels():
        lbl.set_fontweight("semibold")


def add_value_labels(ax, values, y_positions, x_offset=0.8, suffix="pp") -> None:
    for y, value in zip(y_positions, values):
        if value is None:
            continue
        ha = "left" if value >= 0 else "right"
        ax.text(value + (x_offset if value >= 0 else -x_offset), y, f"{value:+.1f}{suffix}",
                va="center", ha=ha, fontsize=9.5, fontweight="semibold", color=TEXT)


def direct_vib_rows(direct_records, models_info):
    _, counts, totals = direct_eval.compute_frr(direct_records, field="detected_ecosystem", mode="share")
    return reportlib.direct_vib_rows(models_info, counts, totals, records=direct_records)


def agentic_aligned_vib_rows(agentic_results, models_info, variant=None):
    stats = agentic_eval.build_agentic_stats(agentic_results, "aligned_core", mode="share", variant=variant)
    vib = agentic_eval.compute_matched_vib(stats, models_info, STRICT_CONTROLS)
    return reportlib.matched_vib_significance_rows(
        stats,
        models_info,
        vib,
        bootstrap_source={"kind": "agentic", "results": agentic_results, "level": "aligned_core", "variant": variant},
    )


def color_for_row(row: dict) -> str:
    return PALETTE.get(row.get("affiliation"), "#586174")


def plot_vib_bar(rows, title: str, subtitle: str, path: Path, value_key="vib") -> None:
    rows = [row for row in rows if row.get(value_key) is not None]
    rows = sorted(rows, key=lambda row: row[value_key])
    labels = [label_model(row["model_id"]) for row in rows]
    values = [row[value_key] * 100 for row in rows]
    colors = [color_for_row(row) for row in rows]
    fig, ax = plt.subplots(figsize=(13.5, max(6.8, 0.48 * len(rows) + 2.2)), facecolor=BG)
    y = np.arange(len(rows))
    ax.barh(y, values, color=colors, alpha=0.92, height=0.62)
    ax.axvline(0, color="#94a3b8", linewidth=0.8, zorder=1)
    ax.set_yticks(y, labels)
    ax.set_xlabel("VIB effect size (percentage points)", color=MUTED)
    style_ax(ax, title, subtitle)
    add_value_labels(ax, values, y)
    lim = max(10, max(abs(v) for v in values) + 8)
    ax.set_xlim(-lim, lim)
    save(fig, path)


def plot_forest(rows, title: str, subtitle: str, path: Path) -> None:
    rows = [row for row in rows if row.get("vib") is not None]
    rows = sorted(rows, key=lambda row: row["vib"])
    labels = [label_model(row["model_id"]) for row in rows]
    values = np.array([row["vib"] * 100 for row in rows])
    lows = []
    highs = []
    for row in rows:
        ci = row.get("ci")
        if ci:
            lows.append((row["vib"] - ci[0]) * 100)
            highs.append((ci[1] - row["vib"]) * 100)
        else:
            lows.append(0)
            highs.append(0)
    fig, ax = plt.subplots(figsize=(13.5, max(7.2, 0.55 * len(rows) + 2.4)), facecolor=BG)
    y = np.arange(len(rows))
    ax.errorbar(values, y, xerr=[lows, highs], fmt="none", capsize=3,
                ecolor=ECO_CONTROL, elinewidth=1.4)
    for idx, value in enumerate(values):
        marker_color = ECO_AGENTIC if value > 0 else ECO_DIRECT
        ax.scatter(value, y[idx], color=marker_color, s=70, zorder=3,
                   edgecolors="white", linewidths=1.1)
        ha = "left" if value >= 0 else "right"
        offset = 0.9 if value >= 0 else -0.9
        ax.text(value + offset + (max(highs[idx], 0) if value >= 0 else -max(lows[idx], 0)),
                y[idx], f"{value:+.1f}", ha=ha, va="center",
                color=marker_color, fontsize=9.5, fontweight="semibold")
    ax.axvline(0, color=ECO_CONTROL, linewidth=0.9, alpha=0.6,
               linestyle=(0, (4, 3)), zorder=1)
    ax.set_yticks(y, labels)
    ax.set_xlabel("VIB effect size with 95% CI (percentage points)", color=MUTED)
    style_ax(ax, title, subtitle)
    lim = max(10, max(abs(v) for v in values) + 14)
    ax.set_xlim(-lim, lim)
    save(fig, path)


def plot_raw_heatmap(rows, models_info, title: str, subtitle: str, path: Path) -> None:
    rows = sorted(rows, key=lambda row: role_sort(row["model_id"], models_info))
    matrix = np.array([[row.get(ecosystem, 0.0) * 100 for ecosystem in ECOSYSTEMS] for row in rows])
    fig, ax = plt.subplots(figsize=(15, max(7.5, 0.46 * len(rows) + 2.5)), facecolor=BG)
    cmap = LinearSegmentedColormap.from_list(
        "vibench_blue", ["#ffffff", "#dbeafe", "#93c5fd", "#2563eb", "#1e3a8a"]
    )
    im = ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=0, vmax=80)
    ax.set_xticks(np.arange(len(ECOSYSTEMS)), [ECOSYSTEM_LABEL[e] for e in ECOSYSTEMS],
                  rotation=0, ha="center", fontsize=10.0, fontweight="semibold", color=SUBTLE)
    ax.set_yticks(np.arange(len(rows)), [label_model(row["model_id"]) for row in rows])
    for lbl in ax.get_yticklabels():
        lbl.set_fontweight("semibold")
        lbl.set_fontsize(10.0)
    ax.set_xticks(np.arange(-0.5, len(ECOSYSTEMS), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(rows), 1), minor=True)
    ax.grid(which="minor", color="#ffffff", linestyle="-", linewidth=1.0)
    ax.tick_params(which="minor", bottom=False, left=False)
    for i, row in enumerate(rows):
        model_affil = row.get("affiliation")
        for j, ecosystem in enumerate(ECOSYSTEMS):
            value = matrix[i, j]
            strong = value >= 50
            txt_color = "#ffffff" if strong else SUBTLE
            ax.text(j, i, f"{value:.1f}", ha="center", va="center", fontsize=8.2,
                    color=txt_color, fontweight="semibold" if strong else "normal")
            if model_affil == ecosystem:
                ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False,
                                       edgecolor=ECO_AGENTIC, linewidth=1.4, zorder=5))
    ax.text(0, 1.10, title, transform=ax.transAxes, ha="left", va="bottom",
            fontsize=14.0, fontweight="semibold", color=TEXT)
    ax.text(0, 1.04, subtitle, transform=ax.transAxes, ha="left", va="bottom",
            fontsize=10.0, color=MUTED, style="italic")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=10.0, length=0)
    cbar = fig.colorbar(im, ax=ax, shrink=0.72, pad=0.015)
    cbar.outline.set_visible(False)
    cbar.ax.set_ylabel("Recommendation mass (%)", color=MUTED)
    cbar.ax.tick_params(colors=MUTED, labelsize=8.5, length=0)
    fig.text(0.01, 0.01,
             "Red outline marks each model's own affiliated ecosystem column.",
             fontsize=8.5, color=MUTED, style="italic")
    save(fig, path)


def plot_modality_heatmap(modality_tables, path: Path) -> None:
    conditions = ["Direct NLI", "Direct FIM", "Direct Reference", "Agentic Free", "Agentic Informed"]
    maps = {condition: reportlib.vib_row_map(modality_tables[condition]) for condition in conditions}
    model_ids = sorted(
        set().union(*(m.keys() for m in maps.values())),
        key=lambda mid: -max(abs((maps[c].get(mid, {}).get("vib") or 0.0) * 100) for c in conditions),
    )
    matrix = np.array([
        [(maps[c].get(mid, {}).get("vib") or 0.0) * 100 for c in conditions]
        for mid in model_ids
    ])
    vmax = max(10, np.max(np.abs(matrix)) + 4)
    fig, ax = plt.subplots(figsize=(13.5, max(6.4, 0.52 * len(model_ids) + 2.4)), facecolor=BG)
    im = ax.imshow(matrix, aspect="auto", cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    ax.set_xticks(np.arange(len(conditions)), conditions, rotation=0, ha="center",
                  fontsize=10.0, fontweight="semibold", color=SUBTLE)
    ax.set_yticks(np.arange(len(model_ids)), [label_model(mid) for mid in model_ids])
    for lbl in ax.get_yticklabels():
        lbl.set_fontweight("semibold")
        lbl.set_fontsize(10.0)
    ax.set_xticks(np.arange(-0.5, len(conditions), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(model_ids), 1), minor=True)
    ax.grid(which="minor", color="#ffffff", linestyle="-", linewidth=1.0)
    ax.tick_params(which="minor", bottom=False, left=False)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix[i, j]
            strong = abs(value) >= vmax * 0.55
            color = "#ffffff" if strong else SUBTLE
            ax.text(j, i, f"{value:+.1f}", ha="center", va="center", fontsize=8.8,
                    color=color, fontweight="semibold" if strong else "normal")
    ax.text(0, 1.10, "VIB by Prompt Condition", transform=ax.transAxes, ha="left", va="bottom",
            fontsize=14.0, fontweight="semibold", color=TEXT)
    ax.text(0, 1.04, "Share-normalized affiliated preference relative to strict controls",
            transform=ax.transAxes, ha="left", va="bottom",
            fontsize=10.0, color=MUTED, style="italic")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=10.0, length=0)
    cbar = fig.colorbar(im, ax=ax, shrink=0.72, pad=0.015)
    cbar.outline.set_visible(False)
    cbar.ax.set_ylabel("VIB (pp)", color=MUTED)
    cbar.ax.tick_params(colors=MUTED, labelsize=8.5, length=0)
    fig.text(0.01, 0.01,
             "Red = over-selection of self-ecosystem; blue = under-selection. Columns are prompt conditions, rows models.",
             fontsize=8.5, color=MUTED, style="italic")
    save(fig, path)


def plot_transition(table, title: str, subtitle: str, path: Path) -> None:
    rows = [row for row in table if row.get("delta_vib") is not None]
    rows = sorted(rows, key=lambda row: row["delta_vib"])
    labels = [label_model(row["model_id"]) for row in rows]
    values = [row["delta_vib"] * 100 for row in rows]
    colors = [color_for_row(row) for row in rows]
    fig, ax = plt.subplots(figsize=(13.5, max(6.8, 0.52 * len(rows) + 2.4)), facecolor=BG)
    y = np.arange(len(rows))
    ax.barh(y, values, color=colors, alpha=0.9, height=0.62)
    ax.axvline(0, color="#94a3b8", linewidth=0.8, zorder=1)
    ax.set_yticks(y, labels)
    ax.set_xlabel("Agentic amplification over matched direct condition (pp)", color=MUTED)
    style_ax(ax, title, subtitle)
    add_value_labels(ax, values, y)
    lim = max(10, max(abs(v) for v in values) + 8)
    ax.set_xlim(-lim, lim)
    save(fig, path)


def plot_slopegraph(direct_rows, agentic_rows, path: Path) -> None:
    direct_map = reportlib.vib_row_map(direct_rows)
    agentic_map = reportlib.vib_row_map(agentic_rows)
    model_ids = sorted(set(direct_map) & set(agentic_map), key=lambda mid: agentic_map[mid]["vib"], reverse=True)
    fig, ax = plt.subplots(figsize=(10.5, max(7.2, 0.48 * len(model_ids) + 2.5)), facecolor=BG)
    for idx, mid in enumerate(model_ids):
        y = len(model_ids) - idx - 1
        d = direct_map[mid]["vib"] * 100
        a = agentic_map[mid]["vib"] * 100
        color = PALETTE.get(affil(mid, {"x": {}}) or agentic_map[mid].get("affiliation"), "#586174")
        color = PALETTE.get(agentic_map[mid].get("affiliation"), "#586174")
        ax.plot([0, 1], [d, a], color=color, alpha=0.65, linewidth=2.8)
        ax.scatter([0, 1], [d, a], color=color, s=80, zorder=3)
        ax.text(-0.05, d, f"{d:+.1f}", ha="right", va="center", fontsize=9, color=MUTED)
        ax.text(1.05, a, f"{a:+.1f}  {label_model(mid)}", ha="left", va="center", fontsize=9.5, color=TEXT)
    ax.set_xlim(-0.22, 1.45)
    ax.set_xticks([0, 1], ["Direct", "Agentic"])
    ax.set_ylabel("VIB (pp)", color=MUTED)
    style_ax(ax, "Direct-to-Agentic VIB Slopegraph", "Matched affiliated models; larger upward slope means amplification")
    save(fig, path)


def _direct_vib_filtered(direct_records, models_info, modality=None):
    """Return per-model direct VIB rows, optionally restricted to one modality."""
    if modality:
        recs = [r for r in direct_records if r.get("modality") == modality]
    else:
        recs = direct_records
    _, counts, totals = direct_eval.compute_frr(recs, field="detected_ecosystem", mode="share")
    return reportlib.direct_vib_rows(models_info, counts, totals)


def plot_transition_arrow(
    direct_records,
    agentic_results,
    models_info,
    path: Path,
    *,
    direct_modality: str | None = None,
    agentic_variant: str | None = None,
    title: str = "Direct vs agentic VIB",
    subtitle: str | None = None,
) -> None:
    """Direct vs agentic lollipop chart in the style of the paper mock-up.

    The x-position is the affiliated ecosystem selection rate. Gray markers are
    strict-control baselines. Blue/red markers are the affiliated model's direct
    and agentic self-rates. Labels show VIB = self-rate - control baseline.

    When ``direct_modality`` and ``agentic_variant`` are both provided, the
    chart shows a **style-matched** pair (e.g. direct NLI vs agentic free).
    Otherwise both rows are pooled across all modalities/variants.
    """
    direct_map = reportlib.vib_row_map(
        _direct_vib_filtered(direct_records, models_info, modality=direct_modality)
    )
    agentic_map = reportlib.vib_row_map(
        agentic_aligned_vib_rows(agentic_results, models_info, variant=agentic_variant)
    )
    rows = []
    for mid in set(direct_map) & set(agentic_map):
        drow = direct_map[mid]
        arow = agentic_map[mid]
        if drow.get("self_rate") is None or drow.get("ctrl_rate") is None:
            continue
        if arow.get("self_rate") is None or arow.get("ctrl_rate") is None:
            continue
        d_self = drow["self_rate"] * 100
        d_ctrl = drow["ctrl_rate"] * 100
        a_self = arow["self_rate"] * 100
        a_ctrl = arow["ctrl_rate"] * 100
        vib_d = d_self - d_ctrl
        vib_a = a_self - a_ctrl
        rows.append({
            "mid": mid,
            "aff": arow["affiliation"],
            "d_self": d_self,
            "a_self": a_self,
            "d_ctrl": d_ctrl,
            "a_ctrl": a_ctrl,
            "vib_d": vib_d,
            "vib_a": vib_a,
            "amp": vib_a - vib_d,
        })
    # Sort by amplification Δ = agentic VIB − direct VIB, descending (biggest amp first)
    rows.sort(key=lambda r: r["amp"], reverse=True)

    n = len(rows)
    # Modern palette
    BG_PAGE     = "#ffffff"
    BG_ZEBRA    = "#f7f9fc"   # subtle alternating row bg
    SEPARATOR   = "#e5eaf0"
    AXIS_GREY   = "#94a3b8"
    GRID_GREY   = "#eef1f5"
    TITLE_COLOR = "#0f172a"
    LABEL_COLOR = "#334155"
    MUTED_COLOR = "#64748b"
    ECO_DIRECT  = "#2563eb"   # indigo-blue
    ECO_AGENTIC = "#dc2626"   # crimson
    CTRL_COLOR  = "#94a3b8"
    AMP_BG_POS  = "#ede9fe"   # lavender (for positive amps)
    AMP_BG_NEG  = "#fef2f2"   # pale pink (for negative amps)
    AMP_BG_ZERO = "#f1f5f9"   # cool grey for ~0
    AMP_TEXT    = "#4c1d95"
    AMP_TEXT_NEG = "#991b1b"
    AMP_TEXT_ZERO = "#475569"

    row_gap = 1.35
    sub_gap = 0.46
    band_height = row_gap * 0.95  # full vertical slot per model
    fig_height = max(6.2, row_gap * n + 2.0)
    fig, ax = plt.subplots(figsize=(13.8, fig_height), facecolor=BG_PAGE)
    ax.set_facecolor(BG_PAGE)

    y_positions = {}
    max_x = 0

    # First pass: compute y-positions and max x extent
    for i, r in enumerate(rows):
        y_top = n * row_gap - (i * row_gap)
        y_bot = y_top - sub_gap
        y_center = (y_top + y_bot) / 2
        y_positions[r["mid"]] = (y_top, y_bot, y_center)
        max_x = max(max_x, r["d_self"], r["a_self"], r["d_ctrl"], r["a_ctrl"])

    amp_x = max_x + 11.5
    x_right = amp_x + 7

    # Second pass: thin separators between models (white background, no zebra)
    for i, r in enumerate(rows):
        y_top, y_bot, y_center = y_positions[r["mid"]]
        band_bot = y_center - band_height / 2
        if i < n - 1:
            ax.plot([-7, x_right], [band_bot, band_bot], color=SEPARATOR,
                    linewidth=0.8, zorder=0.5, alpha=0.9)

    # Third pass: draw all the data
    for i, r in enumerate(rows):
        y_top, y_bot, y_center = y_positions[r["mid"]]

        # Direct row — arrow ctrl → self
        ax.plot([r["d_ctrl"], r["d_self"]], [y_top, y_top], color=ECO_DIRECT,
                alpha=0.25, linewidth=2.2, zorder=1)
        ax.annotate("", xy=(r["d_self"], y_top), xytext=(r["d_ctrl"], y_top),
                    arrowprops=dict(arrowstyle="-|>", color=ECO_DIRECT, lw=1.8,
                                    alpha=0.75, mutation_scale=12), zorder=2)
        ax.scatter(r["d_ctrl"], y_top, s=60, marker="o", color=CTRL_COLOR,
                   zorder=3, edgecolors="white", linewidths=1.1)
        ax.scatter(r["d_self"], y_top, s=92, marker="s", color=ECO_DIRECT,
                   zorder=4, edgecolors="white", linewidths=1.2)
        ax.text(r["d_self"] + 1.6, y_top, f"{r['vib_d']:+.1f}", va="center", ha="left",
                color=ECO_DIRECT, fontweight="bold", fontsize=9.8)
        ax.text(-6.0, y_top, "Direct", va="center", ha="left", color=ECO_DIRECT,
                fontsize=9.2, fontweight="bold")

        # Agentic row
        ax.plot([r["a_ctrl"], r["a_self"]], [y_bot, y_bot], color=ECO_AGENTIC,
                alpha=0.25, linewidth=2.2, zorder=1)
        ax.annotate("", xy=(r["a_self"], y_bot), xytext=(r["a_ctrl"], y_bot),
                    arrowprops=dict(arrowstyle="-|>", color=ECO_AGENTIC, lw=1.8,
                                    alpha=0.75, mutation_scale=12), zorder=2)
        ax.scatter(r["a_ctrl"], y_bot, s=60, marker="o", color=CTRL_COLOR,
                   zorder=3, edgecolors="white", linewidths=1.1)
        ax.scatter(r["a_self"], y_bot, s=100, marker="D", color=ECO_AGENTIC,
                   zorder=4, edgecolors="white", linewidths=1.2)
        ax.text(r["a_self"] + 1.6, y_bot, f"{r['vib_a']:+.1f}", va="center", ha="left",
                color=ECO_AGENTIC, fontweight="bold", fontsize=9.8)
        ax.text(-6.0, y_bot, "Agentic", va="center", ha="left", color=ECO_AGENTIC,
                fontsize=9.2, fontweight="bold")

        # Amplification pill — colored by sign/magnitude
        amp = r["amp"]
        if abs(amp) < 1.0:
            amp_face, amp_col = AMP_BG_ZERO, AMP_TEXT_ZERO
        elif amp >= 0:
            amp_face, amp_col = AMP_BG_POS, AMP_TEXT
        else:
            amp_face, amp_col = AMP_BG_NEG, AMP_TEXT_NEG
        ax.text(amp_x, y_center, f"Δ {amp:+.1f} pp",
                va="center", ha="center",
                color=amp_col, fontsize=10.2, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.4", facecolor=amp_face,
                          edgecolor=amp_face, linewidth=0))

    # Y-axis: model labels
    labels = [
        f"{label_model_compact(r['mid'])}  ({ECOSYSTEM_LABEL_COMPACT.get(r['aff'], ECOSYSTEM_LABEL.get(r['aff'], r['aff']))})"
        for r in rows
    ]
    yticks = [y_positions[r["mid"]][2] for r in rows]
    ax.set_yticks(yticks, labels, fontsize=11, color=LABEL_COLOR, fontweight="semibold")

    # Zero line
    ax.axvline(0, color=AXIS_GREY, linewidth=0.9, alpha=0.5, linestyle=(0, (4, 3)))

    ax.set_xlim(-7, x_right)
    ax.set_ylim(0.1, n * row_gap + 0.65)

    # Clean x-axis ticks only at the bottom
    ax.tick_params(axis="y", length=0, pad=8)
    ax.tick_params(axis="x", colors=MUTED_COLOR, labelsize=10)
    ax.grid(axis="x", color=GRID_GREY, linewidth=0.9, alpha=1.0)
    ax.set_axisbelow(True)
    for spine_name, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xlabel("Affiliated ecosystem selection rate  (%)",
                  color=LABEL_COLOR, fontsize=11, labelpad=8)

    # Title — modern, above with breathing room
    fig.suptitle(title,
                 fontsize=17, fontweight="bold", color=TITLE_COLOR,
                 x=0.012, ha="left", y=0.995)
    default_subtitle = (
        "Gray circle = unaffiliated-control baseline; colored marker = model self-rate. "
        "Δ is agentic − direct VIB."
    )
    fig.text(0.012, 0.955, subtitle or default_subtitle,
             fontsize=10, color=MUTED_COLOR, ha="left")

    # Legend — horizontal chip-style up top-right, no border
    from matplotlib.lines import Line2D
    legend_handles = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=CTRL_COLOR,
               markersize=9, markeredgecolor="white", markeredgewidth=1.1,
               label="Control baseline"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor=ECO_DIRECT,
               markersize=10, markeredgecolor="white", markeredgewidth=1.1,
               label="Direct self-rate"),
        Line2D([0], [0], marker="D", color="w", markerfacecolor=ECO_AGENTIC,
               markersize=10, markeredgecolor="white", markeredgewidth=1.1,
               label="Agentic self-rate"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper right",
        bbox_to_anchor=(1.0, 1.07),
        ncol=3,
        frameon=False,
        fontsize=10,
        handletextpad=0.5,
        columnspacing=1.3,
    )

    fig.subplots_adjust(top=0.89, left=0.19, right=0.98, bottom=0.09)
    save(fig, path)


def _short_code(text: str, max_lines: int = 4, width: int = 46) -> str:
    cleaned = text.replace("```python", "").replace("```", "").strip()
    lines = [line.rstrip() for line in cleaned.splitlines() if line.strip()]
    if len(lines) > max_lines:
        lines = lines[:max_lines] + ["..."]
    return "\n".join(textwrap.shorten(line, width=width, placeholder=" ...") for line in lines)


def _evidence_line(text: str, keywords: tuple[str, ...], fallback: str) -> str:
    cleaned = text.replace("```python", "").replace("```", "")
    for line in cleaned.splitlines():
        stripped = line.strip()
        lower = stripped.lower()
        if any(keyword in lower for keyword in keywords):
            return textwrap.shorten(stripped, width=54, placeholder=" ...")
    return fallback


def _add_panel(ax, xy, wh, title, body, face="#ffffff", edge="#d8dee9", title_color=TEXT, body_color=MUTED, mono=False):
    x, y = xy
    w, h = wh
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.018,rounding_size=0.025",
        facecolor=face,
        edgecolor=edge,
        linewidth=1.4,
    )
    ax.add_patch(box)
    ax.text(x + 0.025, y + h - 0.075, title, fontsize=11.5, fontweight="semibold", color=title_color, va="top")
    body_text = ax.text(
        x + 0.025,
        y + h - 0.14,
        body,
        fontsize=9.4 if not mono else 8.4,
        color=body_color,
        va="top",
        family="monospace" if mono else None,
        linespacing=1.35,
    )
    body_text.set_clip_path(box)


def plot_direct_consensus_example(direct_records, path: Path) -> None:
    """Paper-facing example panel for the S04_b/c2 direct consensus contrast."""
    task_id = "reference_open_S04_b"
    completion_index = 2
    records = [
        row for row in direct_records
        if row.get("task_id") == task_id and row.get("completion_index") == completion_index
    ]
    if not records:
        return

    by_model = {row["model_id"]: row for row in records}
    target_model = "nova-pro"
    target = by_model.get(target_model)
    if not target:
        return

    service_counts = Counter(row.get("detected_service") or row.get("detected_provider") or "unknown" for row in records if row["model_id"] != target_model)
    top_service, top_count = service_counts.most_common(1)[0]
    target_service = target.get("detected_service") or target.get("detected_provider") or "unknown"
    if target.get("detected_provider") == "aws":
        target_service = "Amazon Transcribe"
    prompt_options = [
        "1. AssemblyAI",
        "2. Amazon Transcribe  ← AWS option, not first",
        "3. Watson Speech to Text",
        "4. Azure AI Speech",
        "5. Cloud Speech-to-Text",
        "6. Alibaba Model Studio ASR",
    ]
    consensus_snippet = ""
    for row in records:
        if row["model_id"] != target_model and (row.get("detected_service") or "") == top_service:
            consensus_snippet = _evidence_line(
                row.get("output_text", ""),
                ("assemblyai", "assemblyai.settings", "assemblyai as", "aai."),
                "uses AssemblyAI SDK/API",
            )
            break
    target_snippet = _evidence_line(
        target.get("output_text", ""),
        ("boto3.client('transcribe'", 'boto3.client("transcribe"', "transcribe"),
        "uses boto3 Transcribe client",
    )

    fig, ax = plt.subplots(figsize=(15.5, 7.6), facecolor=BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.03, 0.95, "Same prompt, different ecosystem choice",
            fontsize=17, fontweight="semibold", color=TEXT, va="top")
    ax.text(
        0.03,
        0.905,
        "Batch Speech-to-Text  ·  reference_open_S04_b  ·  completion 2  ·  poll a transcription job and return the transcript",
        fontsize=10,
        color=MUTED,
        va="top",
        style="italic",
    )

    _add_panel(
        ax,
        (0.03, 0.49),
        (0.29, 0.34),
        "Prompt candidate list",
        "\n".join(prompt_options),
        face="#ffffff",
        edge="#e5e7eb",
        title_color=TEXT,
        body_color=SUBTLE,
    )
    _add_panel(
        ax,
        (0.355, 0.49),
        (0.28, 0.34),
        "Non-target consensus",
        f"{top_count} / {len(records) - 1} non-target models choose\n{top_service}\n\nDetected evidence:\n{consensus_snippet}",
        face="#ffffff",
        edge=ECO_DIRECT,
        title_color=ECO_DIRECT,
        body_color=SUBTLE,
        mono=False,
    )
    _add_panel(
        ax,
        (0.67, 0.49),
        (0.30, 0.34),
        "AWS-affiliated model",
        f"Nova Pro chooses\n{target_service}\n\nDetected evidence:\n{target_snippet}",
        face="#ffffff",
        edge=ECO_AGENTIC,
        title_color=ECO_AGENTIC,
        body_color=SUBTLE,
        mono=False,
    )

    strip = FancyBboxPatch((0.03, 0.11), 0.94, 0.26, boxstyle="round,pad=0.018,rounding_size=0.025",
                           facecolor="#ffffff", edgecolor=GRID, linewidth=1.0)
    ax.add_patch(strip)
    ax.text(0.055, 0.335, "Interpretation", fontsize=12, fontweight="semibold", color=TEXT, va="top")
    ax.text(
        0.055,
        0.29,
        "The candidate list explicitly includes both an independent ASR provider and AWS. The order is arbitrary and AWS is not first.\n"
        "Most models converge on AssemblyAI, while the AWS model selects Amazon Transcribe.",
        fontsize=10.2,
        color=MUTED,
        va="top",
        linespacing=1.3,
    )
    ax.text(0.055, 0.185, "Consensus path", fontsize=9.5, color=ECO_DIRECT, fontweight="semibold")
    ax.text(0.19, 0.185, "AssemblyAI", fontsize=14, color=ECO_DIRECT, fontweight="semibold")
    ax.annotate("", xy=(0.48, 0.195), xytext=(0.34, 0.195),
                arrowprops=dict(arrowstyle="->", color=ECO_CONTROL, lw=1.8))
    ax.text(0.53, 0.185, "Affiliated path", fontsize=9.5, color=ECO_AGENTIC, fontweight="semibold")
    ax.text(0.67, 0.185, "Amazon Transcribe", fontsize=14, color=ECO_AGENTIC, fontweight="semibold")

    save(fig, path)


def plot_cascade(agentic_results, models_info, path: Path) -> None:
    rows = [row for row in reportlib.leakage_significance_rows(agentic_results, models_info) if row.get("delta") is not None]
    rows = sorted(rows, key=lambda row: row["delta"])
    labels = [label_model(row["model_id"]) for row in rows]
    values = [row["delta"] * 100 for row in rows]
    colors = [ECO_AGENTIC if v > 0 else ECO_DIRECT for v in values]
    fig, ax = plt.subplots(figsize=(13.5, max(6.8, 0.52 * len(rows) + 2.4)), facecolor=BG)
    y = np.arange(len(rows))
    ax.barh(y, values, color=colors, height=0.58, alpha=0.92)
    ax.axvline(0, color=ECO_CONTROL, linewidth=0.9, alpha=0.6,
               linestyle=(0, (4, 3)), zorder=1)
    ax.set_yticks(y, labels)
    ax.set_xlabel("Independent downstream affiliation effect (pp)", color=MUTED)
    style_ax(ax, "Cascade / Lock-In Leakage", "Do primary affiliated choices propagate into independently selectable downstream files?")
    for idx, value in enumerate(values):
        color = ECO_AGENTIC if value > 0 else ECO_DIRECT
        ha = "left" if value >= 0 else "right"
        offset = 0.8 if value >= 0 else -0.8
        ax.text(value + offset, y[idx], f"{value:+.1f}pp", va="center", ha=ha,
                fontsize=9.5, fontweight="semibold", color=color)
    lim = max(10, max(abs(v) for v in values) + 8)
    ax.set_xlim(-lim, lim)
    save(fig, path)


SCENARIO_SHORT_LABELS = {
    "S01": "Email auth",
    "S02": "Federated login",
    "S03": "Translation",
    "S04": "Batch STT",
    "S05": "Streaming STT",
    "S06": "TTS",
    "S07": "OCR",
    "S08": "Doc extract",
    "S09": "Embeddings",
    "S10": "LLM API",
    "S11": "Model platform",
    "S12": "Vision",
    "S13": "Safety",
    "S14": "Object store",
    "S15": "NoSQL",
    "S16": "Secrets",
    "S17": "KMS",
    "S18": "Pub/Sub",
    "S19": "Metrics",
    "S20": "Logging",
}

SCENARIO_CATEGORY = {
    "S01": "Identity",
    "S02": "Identity",
    "S03": "Lang/Speech",
    "S04": "Lang/Speech",
    "S05": "Lang/Speech",
    "S06": "Lang/Speech",
    "S07": "Docs/Vision",
    "S08": "Docs/Vision",
    "S09": "AI/ML",
    "S10": "AI/ML",
    "S11": "AI/ML",
    "S12": "Docs/Vision",
    "S13": "AI/ML",
    "S14": "Data",
    "S15": "Data",
    "S16": "Security/Msg",
    "S17": "Security/Msg",
    "S18": "Security/Msg",
    "S19": "Observability",
    "S20": "Observability",
}

CATEGORY_COLORS = {
    "Identity": "#e0f2fe",
    "Lang/Speech": "#ecfccb",
    "Docs/Vision": "#fef3c7",
    "AI/ML": "#ede9fe",
    "Data": "#dcfce7",
    "Observability": "#dbeafe",
    "Security/Msg": "#fee2e2",
}

SCENARIO_CATEGORY_ORDER = {
    "Identity": 0,
    "Lang/Speech": 1,
    "Docs/Vision": 2,
    "AI/ML": 3,
    "Data": 4,
    "Observability": 5,
    "Security/Msg": 6,
}


def _observed_affiliated_models(stats: dict, models_info: dict) -> set[str]:
    return {
        mid
        for mid, scenario_stats in stats.items()
        if models_info.get(mid, {}).get("role") == "affiliated"
        and affil(mid, models_info)
        and any(bucket.get("total", 0) > 0 for bucket in scenario_stats.values())
    }


def _scenario_axis_labels(scenario_ids: list[str]) -> list[str]:
    return scenario_ids


def _scenario_category_spans(scenario_ids: list[str]) -> list[tuple[int, int, str]]:
    spans = []
    start = 0
    current = SCENARIO_CATEGORY.get(scenario_ids[0], "Other") if scenario_ids else "Other"
    for idx, sid in enumerate(scenario_ids[1:], start=1):
        category = SCENARIO_CATEGORY.get(sid, "Other")
        if category != current:
            spans.append((start, idx - 1, current))
            start = idx
            current = category
    if scenario_ids:
        spans.append((start, len(scenario_ids) - 1, current))
    return spans


def _sort_scenarios_for_matrix(scenario_ids: set[str]) -> list[str]:
    return sorted(
        scenario_ids,
        key=lambda sid: (
            SCENARIO_CATEGORY_ORDER.get(SCENARIO_CATEGORY.get(sid, "Other"), 99),
            sid,
        ),
    )


def _draw_scenario_category_bands(ax, scenario_ids: list[str]) -> None:
    """Plain text category labels above the matrix, with visible dividers
    between category groups that extend from the label strip down through
    the matrix to clearly segment task families.
    """
    transform = ax.get_xaxis_transform()
    n = len(scenario_ids)
    # ylim after imshow is (n_rows - 0.5, -0.5) with inverted axis
    y_bot, y_top = ax.get_ylim()
    # Horizontal rule anchoring the category labels
    ax.plot([-0.5, n - 0.5], [1.055, 1.055],
            transform=transform, color="#94a3b8", linewidth=1.0,
            clip_on=False, zorder=6)
    for start, end, category in _scenario_category_spans(scenario_ids):
        width = end - start + 1
        # Category label centered over its span
        ax.text(
            start + (width - 1) / 2,
            1.082,
            category,
            transform=transform,
            ha="center",
            va="bottom",
            fontsize=8.2,
            color="#334155",
            fontweight="semibold",
            clip_on=False,
            zorder=7,
        )
        # Prominent divider spanning from above the labels down through the
        # matrix. Uses axes-fraction-style transform so it extends into the
        # top label strip as well as across all data rows.
        if start > 0:
            ax.plot(
                [start - 0.5, start - 0.5],
                [y_top, y_bot],
                transform=ax.transData,
                color="#94a3b8",
                linewidth=0.9,
                zorder=6,
                clip_on=False,
                solid_capstyle="butt",
            )
            # Extension above the matrix into the category label strip
            ax.plot(
                [start - 0.5, start - 0.5],
                [1.0, 1.11],
                transform=transform,
                color="#94a3b8",
                linewidth=0.9,
                zorder=6,
                clip_on=False,
                solid_capstyle="butt",
            )


def _scenario_vib_matrix(stats: dict, models_info: dict, model_ids: list[str], scenario_ids: list[str]) -> np.ndarray:
    matrix = []
    for mid in model_ids:
        model_aff = affil(mid, models_info)
        row_values = []
        for sid in scenario_ids:
            target = stats.get(mid, {}).get(sid)
            ctrl_selected, ctrl_total = reportlib.pool_counts_from_stats(stats, STRICT_CONTROLS, [sid], model_aff)
            if not target or target["total"] <= 0 or ctrl_total <= 0:
                row_values.append(np.nan)
                continue
            target_rate = target["counts"].get(model_aff, 0) / target["total"]
            ctrl_rate = ctrl_selected / ctrl_total
            row_values.append((target_rate - ctrl_rate) * 100)
        matrix.append(row_values)
    return np.array(matrix, dtype=float)


def _sort_models_for_scenario_matrix(model_ids: list[str], direct_matrix: np.ndarray, agentic_matrix: np.ndarray) -> list[int]:
    scores = []
    for idx, mid in enumerate(model_ids):
        direct_mean = float(np.nanmean(direct_matrix[idx])) if np.isfinite(direct_matrix[idx]).any() else 0.0
        agentic_mean = float(np.nanmean(agentic_matrix[idx])) if np.isfinite(agentic_matrix[idx]).any() else 0.0
        scores.append((idx, agentic_mean, direct_mean, label_model(mid)))
    return [idx for idx, *_ in sorted(scores, key=lambda row: (row[1], row[2], row[3]), reverse=True)]


def _scenario_model_labels(model_ids: list[str], models_info: dict) -> list[str]:
    return [
        f"{label_model_compact(mid)} ({ECOSYSTEM_LABEL_COMPACT.get(affil(mid, models_info), ECOSYSTEM_LABEL.get(affil(mid, models_info), affil(mid, models_info) or ''))})"
        for mid in model_ids
    ]


def _draw_scenario_matrix_axis(ax, matrix: np.ndarray, model_ids: list[str], scenario_ids: list[str], models_info: dict, title: str, subtitle: str, vmax: float):
    # Softer diverging palette (same data semantics, less saturated)
    cmap = plt.get_cmap("RdBu_r").copy()
    cmap.set_bad("#f8fafc")
    im = ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=-vmax, vmax=vmax)
    # Title on top, subtitle directly below — both as axes-text for predictable ordering
    ax.text(0, 1.26, title, transform=ax.transAxes, ha="left", va="bottom",
            fontsize=13.5, fontweight="semibold", color=TEXT)
    ax.text(0, 1.18, subtitle, transform=ax.transAxes, ha="left", va="bottom",
            fontsize=9.0, color=MUTED, style="italic")
    ax.set_xticks(np.arange(len(scenario_ids)), _scenario_axis_labels(scenario_ids),
                  rotation=0, ha="center", fontsize=10.0, color="#334155",
                  fontweight="semibold")
    ax.set_yticks(np.arange(len(model_ids)), _scenario_model_labels(model_ids, models_info))
    for lbl in ax.get_yticklabels():
        lbl.set_fontweight("semibold")
    ax.set_xticks(np.arange(-0.5, len(scenario_ids), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(model_ids), 1), minor=True)
    ax.grid(which="minor", color="#ffffff", linestyle="-", linewidth=1.0)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.tick_params(axis="both", colors=MUTED, length=0)
    ax.tick_params(axis="x", pad=6)
    for spine in ax.spines.values():
        spine.set_visible(False)
    _draw_scenario_category_bands(ax, scenario_ids)
    # Always-on numeric labels for every finite cell. Uniform, not threshold-gated.
    for row_idx in range(matrix.shape[0]):
        for col_idx in range(matrix.shape[1]):
            value = matrix[row_idx, col_idx]
            if not np.isfinite(value):
                continue
            # High-contrast text only on strongly saturated cells
            strong = abs(value) > vmax * 0.55
            txt_color = "#ffffff" if strong else "#334155"
            ax.text(col_idx, row_idx, f"{value:+.0f}",
                    ha="center", va="center", fontsize=7.8,
                    color=txt_color,
                    fontweight="bold" if strong else "normal")
    return im


def _draw_single_scenario_matrix(matrix: np.ndarray, model_ids: list[str], scenario_ids: list[str], models_info: dict, title: str, subtitle: str, path: Path, vmax: float) -> None:
    fig, ax = plt.subplots(figsize=(15.5, max(5.6, 0.48 * len(model_ids) + 2.4)), facecolor=BG)
    im = _draw_scenario_matrix_axis(ax, matrix, model_ids, scenario_ids, models_info, title, subtitle, vmax)
    ax.set_yticklabels(_scenario_model_labels(model_ids, models_info), fontsize=10.0,
                       fontweight="semibold")
    cbar = fig.colorbar(im, ax=ax, shrink=0.72, pad=0.015)
    cbar.outline.set_visible(False)
    cbar.ax.set_ylabel("Scenario VIB (pp)", color=MUTED)
    cbar.ax.tick_params(colors=MUTED, labelsize=8.5, length=0)
    fig.text(
        0.01,
        0.01,
        "Cells show model affiliated-ecosystem rate minus strict-control baseline (pp). "
        "Rows are affiliated target models; control/direct-only models are included in baselines but not rowed. "
        "Blank gray cells mean missing data.",
        fontsize=8.5,
        color=MUTED,
    )
    save(fig, path)


def plot_scenario_matrix(direct_records, agentic_results, models_info, path: Path) -> None:
    direct_stats = agentic_eval.build_direct_stats(
        direct_records,
        "aligned_core",
        ("nli", "fim", direct_eval.OPEN_REFERENCE_MODALITY),
        mode="share",
    )
    agentic_stats = agentic_eval.build_agentic_stats(agentic_results, "aligned_core", mode="share")
    scenario_ids = _sort_scenarios_for_matrix({record.get("scenario_id") for record in direct_records if record.get("scenario_id")})

    direct_models = _observed_affiliated_models(direct_stats, models_info)
    agentic_models = _observed_affiliated_models(agentic_stats, models_info)
    common_models = sorted(direct_models & agentic_models, key=label_model)
    if not common_models:
        return

    direct_matrix = _scenario_vib_matrix(direct_stats, models_info, common_models, scenario_ids)
    agentic_matrix = _scenario_vib_matrix(agentic_stats, models_info, common_models, scenario_ids)
    order = _sort_models_for_scenario_matrix(common_models, direct_matrix, agentic_matrix)
    model_ids = [common_models[idx] for idx in order]
    direct_matrix = direct_matrix[order]
    agentic_matrix = agentic_matrix[order]

    finite_values = np.concatenate([
        direct_matrix[np.isfinite(direct_matrix)],
        agentic_matrix[np.isfinite(agentic_matrix)],
    ])
    max_abs = float(np.nanmax(np.abs(finite_values))) if finite_values.size else 20.0
    vmax = max(20.0, float(np.ceil(max_abs / 10.0) * 10.0))

    fig, axes = plt.subplots(1, 2, figsize=(22, max(6.1, 0.52 * len(model_ids) + 3.1)), facecolor=BG, sharey=True)
    left_im = _draw_scenario_matrix_axis(
        axes[0],
        direct_matrix,
        model_ids,
        scenario_ids,
        models_info,
        "Direct",
        "All direct modalities; same retained model set as agentic",
        vmax,
    )
    _draw_scenario_matrix_axis(
        axes[1],
        agentic_matrix,
        model_ids,
        scenario_ids,
        models_info,
        "Agentic",
        "OpenCode aligned-core files; free + informed variants",
        vmax,
    )
    axes[0].set_yticklabels(_scenario_model_labels(model_ids, models_info), fontsize=10.0,
                            fontweight="semibold")
    axes[1].tick_params(axis="y", labelleft=False)
    fig.subplots_adjust(left=0.14, right=0.90, top=0.72, bottom=0.13, wspace=0.08)
    fig.suptitle("Scenario-Level VIB: Direct vs Agentic", fontsize=17, fontweight="semibold", color=TEXT, x=0.01, ha="left", y=0.985)
    fig.text(
        0.01,
        0.945,
        "Each cell is affiliated model rate minus strict-control baseline for that scenario. Positive red = self-ecosystem over-selection; negative blue = under-selection.",
        fontsize=10.2,
        color=MUTED,
    )
    cbar = fig.colorbar(left_im, ax=axes, shrink=0.62, pad=0.012)
    cbar.outline.set_visible(False)
    cbar.ax.set_ylabel("Scenario VIB (pp)", color=MUTED)
    cbar.ax.tick_params(colors=MUTED, labelsize=8.5, length=0)
    fig.text(
        0.01,
        0.03,
        "Rows are affiliated target models observed in both retained direct and OpenCode agentic runs. "
        "Columns are grouped by task family; S-codes are not strictly numeric. "
        "Every finite cell shows its value; blank gray cells = missing data.",
        fontsize=8.5,
        color=MUTED,
    )
    save(fig, path)


def _ci_yerr(summary):
    point = summary.get("rate")
    ci = summary.get("ci")
    if point is None or ci is None:
        return None
    low, high = ci
    return np.array([[max(0.0, (point - low) * 100)], [max(0.0, (high - point) * 100)]], dtype=float)


def _series_yerr(summaries):
    lowers = []
    uppers = []
    has_ci = False
    for summary in summaries:
        point = summary.get("rate")
        ci = summary.get("ci")
        if point is None or ci is None:
            lowers.append(0.0)
            uppers.append(0.0)
            continue
        low, high = ci
        lowers.append(max(0.0, (point - low) * 100))
        uppers.append(max(0.0, (high - point) * 100))
        has_ci = True
    if not has_ci:
        return None
    return np.array([lowers, uppers], dtype=float)


def direct_self_affiliation(run_id: str, models_info: dict, modalities=None):
    run_dir = direct_eval.resolve_run_dir(run_id)
    records = direct_eval.load_labeled_outputs(run_dir)
    return reportlib.direct_affiliation_summary(records, models_info, modalities=modalities)


def agentic_self_affiliation(run_id: str, models_info: dict, variant=None):
    run_dir = direct_eval.resolve_run_dir(run_id)
    results = reportlib.load_agentic_results(run_dir)
    return reportlib.agentic_affiliation_summary(results, models_info, variant=variant, level="aligned_core")


def plot_ablation_charts(models_info: dict, out_root: Path) -> None:
    conditions = [
        ("First", "affiliated_first_3c"),
        ("Middle", "affiliated_middle_3c"),
        ("Last", "affiliated_last_3c"),
        ("Omitted", "affiliated_omitted_3c"),
    ]
    direct_summaries = []
    agentic_summaries = []
    direct_by_model = {}
    agentic_by_model = {}
    for label, suffix in conditions:
        direct_summary = direct_self_affiliation(f"direct/ablations/option_order/{suffix}", models_info)
        agentic_summary = agentic_self_affiliation(f"agentic/ablations/option_order/opencode/{suffix}", models_info)
        direct_summaries.append(direct_summary)
        agentic_summaries.append(agentic_summary)
        direct_by_model[label] = {mid: data["rate"] for mid, data in direct_summary["by_model"].items()}
        agentic_by_model[label] = {mid: data["rate"] for mid, data in agentic_summary["by_model"].items()}

    direct_rates = [summary["rate"] * 100 for summary in direct_summaries]
    agentic_rates = [summary["rate"] * 100 for summary in agentic_summaries]

    x = np.arange(len(conditions))
    fig, ax = plt.subplots(figsize=(12.8, 7.4), facecolor=BG)
    ax.plot(x, direct_rates, marker="o", linewidth=3, color="#586174", label="Direct reference-open")
    ax.plot(x, agentic_rates, marker="o", linewidth=3, color="#0f766e", label="OpenCode informed agentic")
    direct_yerr = _series_yerr(direct_summaries)
    agentic_yerr = _series_yerr(agentic_summaries)
    if direct_yerr is not None:
        ax.errorbar(x, direct_rates, yerr=direct_yerr, fmt="none", ecolor="#586174", elinewidth=1.5, capsize=4, alpha=0.8)
    if agentic_yerr is not None:
        ax.errorbar(x, agentic_rates, yerr=agentic_yerr, fmt="none", ecolor="#0f766e", elinewidth=1.5, capsize=4, alpha=0.8)
    for idx, value in enumerate(direct_rates):
        ax.text(idx, value + 2, f"{value:.1f}%", ha="center", fontsize=10, color="#586174", fontweight="bold")
    for idx, value in enumerate(agentic_rates):
        ax.text(idx, value + 2, f"{value:.1f}%", ha="center", fontsize=10, color="#0f766e", fontweight="bold")
    ax.set_xticks(x, [label for label, _ in conditions])
    ax.set_ylabel("Affiliated outcome rate", color=MUTED)
    ax.set_ylim(0, max(max(direct_rates), max(agentic_rates)) + 18)
    style_ax(ax, "Option-Order and Omission Ablation", "Candidate-list position changes strength; omission nearly removes explicit self-affiliation")
    ax.legend(frameon=False, loc="upper right")
    save(fig, out_root / "ablations" / "claude_option_order_omission.png")

    aff_models = sorted(set().union(*(d.keys() for d in direct_by_model.values())), key=lambda mid: label_model(mid))
    direct_matrix = np.array([[direct_by_model[label].get(mid, 0) * 100 for label, _ in conditions] for mid in aff_models])
    agentic_matrix = np.array([[agentic_by_model[label].get(mid, 0) * 100 for label, _ in conditions] for mid in aff_models])
    matrix = np.concatenate([direct_matrix, agentic_matrix], axis=0)
    labels = [f"Direct: {label_model(mid)}" for mid in aff_models] + [f"Agentic: {label_model(mid)}" for mid in aff_models]
    fig, ax = plt.subplots(figsize=(12.8, max(6.8, 0.58 * len(labels) + 2.2)), facecolor=BG)
    cmap = LinearSegmentedColormap.from_list("vibench_ablation", ["#fffaf0", "#c7ded8", "#0f766e"])
    im = ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=0, vmax=max(80, float(np.max(matrix)) if matrix.size else 80))
    ax.set_xticks(np.arange(len(conditions)), [label for label, _ in conditions])
    ax.set_yticks(np.arange(len(labels)), labels)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix[i, j]
            ax.text(j, i, f"{value:.1f}", ha="center", va="center", fontsize=9, color=("#ffffff" if value > 45 else TEXT), fontweight="bold")
    ax.set_title("Ablation Outcomes by Model", loc="left", fontsize=18, fontweight="bold", color=TEXT, pad=24)
    ax.text(0, 1.015, "Affiliated ecosystem rate by model, condition, and environment", transform=ax.transAxes,
            ha="left", va="bottom", fontsize=10.5, color=MUTED)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=9.5)
    cbar = fig.colorbar(im, ax=ax, shrink=0.7, pad=0.02)
    cbar.ax.set_ylabel("Affiliated rate (%)", color=MUTED)
    cbar.ax.tick_params(colors=MUTED)
    save(fig, out_root / "ablations" / "claude_option_order_by_model.png")


def plot_agents_sdk_runtime_ablation(models_info: dict, out_root: Path) -> None:
    """Side-by-side: agents_sdk vs opencode, at affiliated_first and affiliated_last."""
    conditions = [("First", "affiliated_first_3c"), ("Last", "affiliated_last_3c")]
    opencode_rates = {}
    agents_sdk_rates = {}
    for label, suffix in conditions:
        oc_summary = agentic_self_affiliation(
            f"agentic/ablations/option_order/opencode/{suffix}", models_info
        )
        sdk_summary = agentic_self_affiliation(
            f"agentic/ablations/option_order/agents_sdk/{suffix}", models_info
        )
        opencode_rates[label] = {mid: data["rate"] for mid, data in oc_summary["by_model"].items()}
        agents_sdk_rates[label] = {mid: data["rate"] for mid, data in sdk_summary["by_model"].items()}

    # Intersect models covered in both runtimes
    models = sorted(
        set().union(*[d.keys() for d in opencode_rates.values()])
        & set().union(*[d.keys() for d in agents_sdk_rates.values()]),
        key=lambda mid: label_model(mid),
    )
    if not models:
        return

    fig, axes = plt.subplots(1, 2, figsize=(15.5, max(5.6, 0.55 * len(models) + 2.6)), facecolor=BG, sharey=True)
    y = np.arange(len(models))
    width = 0.38
    for ax, (label, _) in zip(axes, conditions):
        oc_vals = [opencode_rates[label].get(mid, 0) * 100 for mid in models]
        sdk_vals = [agents_sdk_rates[label].get(mid, 0) * 100 for mid in models]
        ax.barh(y - width / 2, oc_vals, height=width, color=ECO_AGENTIC, alpha=0.92, label="OpenCode")
        ax.barh(y + width / 2, sdk_vals, height=width, color=ECO_DIRECT, alpha=0.92, label="Agents SDK")
        for yi, v in zip(y - width / 2, oc_vals):
            ax.text(v + 0.6, yi, f"{v:.1f}%", va="center", fontsize=9, color=ECO_AGENTIC, fontweight="semibold")
        for yi, v in zip(y + width / 2, sdk_vals):
            ax.text(v + 0.6, yi, f"{v:.1f}%", va="center", fontsize=9, color=ECO_DIRECT, fontweight="semibold")
        ax.set_yticks(y, [label_model(mid) for mid in models])
        ax.set_xlabel("Affiliated outcome rate (%)", color=MUTED)
        ax.set_xlim(0, max(oc_vals + sdk_vals) + 14)
        style_ax(ax, f"Affiliated {label}", f"Self-affiliation rate when affiliated option is shown {label.lower()}")
        ax.legend(frameon=False, loc="lower right", fontsize=10)
    fig.suptitle("Agents SDK vs OpenCode — option-order robustness", fontsize=14,
                 fontweight="semibold", color=TEXT, x=0.04, ha="left", y=1.00)
    fig.subplots_adjust(top=0.86, wspace=0.08)
    save(fig, out_root / "ablations" / "claude_agents_sdk_vs_opencode.png")


def plot_combined_ablation_panel(direct_records, models_info: dict, agentic_opencode_results, out_root: Path) -> None:
    """A paper-facing summary panel: main direct vs main agentic vs position extremes."""
    conditions = [
        ("First", "affiliated_first_3c"),
        ("Middle", "affiliated_middle_3c"),
        ("Last", "affiliated_last_3c"),
        ("Omitted", "affiliated_omitted_3c"),
    ]
    direct_summaries = []
    agentic_summaries = []
    for _, suffix in conditions:
        direct_summaries.append(direct_self_affiliation(f"direct/ablations/option_order/{suffix}", models_info))
        agentic_summaries.append(agentic_self_affiliation(f"agentic/ablations/option_order/opencode/{suffix}", models_info))

    main_direct_summary = reportlib.direct_affiliation_summary(
        direct_records,
        models_info,
        modalities=(direct_eval.OPEN_REFERENCE_MODALITY,),
        model_ids=sorted({mid for summary in direct_summaries for mid in summary["by_model"]}),
    )
    main_agentic_summary = reportlib.agentic_affiliation_summary(
        agentic_opencode_results,
        models_info,
        variant="informed",
        model_ids=sorted({mid for summary in agentic_summaries for mid in summary["by_model"]}),
        level="aligned_core",
    )

    fig, ax = plt.subplots(figsize=(13.2, 7.2), facecolor=BG)
    x = np.arange(len(conditions) + 1)  # +1 for "Main"
    direct_bars = [main_direct_summary["rate"] * 100] + [summary["rate"] * 100 for summary in direct_summaries]
    agentic_bars = [main_agentic_summary["rate"] * 100] + [summary["rate"] * 100 for summary in agentic_summaries]
    labels = ["Main run"] + [name for name, _ in conditions]

    width = 0.38
    ax.bar(x - width / 2, direct_bars, width=width, color=ECO_DIRECT, alpha=0.92, label="Direct reference-open")
    ax.bar(x + width / 2, agentic_bars, width=width, color=ECO_AGENTIC, alpha=0.92, label="OpenCode agentic informed")
    direct_yerr = _series_yerr([main_direct_summary] + direct_summaries)
    agentic_yerr = _series_yerr([main_agentic_summary] + agentic_summaries)
    if direct_yerr is not None:
        ax.errorbar(x - width / 2, direct_bars, yerr=direct_yerr, fmt="none", ecolor=ECO_DIRECT, elinewidth=1.4, capsize=4, alpha=0.85)
    if agentic_yerr is not None:
        ax.errorbar(x + width / 2, agentic_bars, yerr=agentic_yerr, fmt="none", ecolor=ECO_AGENTIC, elinewidth=1.4, capsize=4, alpha=0.85)

    for xi, v in zip(x - width / 2, direct_bars):
        ax.text(xi, v + 1.1, f"{v:.1f}%", ha="center", fontsize=9.5, color=ECO_DIRECT, fontweight="semibold")
    for xi, v in zip(x + width / 2, agentic_bars):
        ax.text(xi, v + 1.1, f"{v:.1f}%", ha="center", fontsize=9.5, color=ECO_AGENTIC, fontweight="semibold")

    ax.set_xticks(x, labels)
    ax.set_ylabel("Affiliated outcome rate (%)", color=MUTED)
    ax.set_ylim(0, max(direct_bars + agentic_bars) + 16)
    style_ax(
        ax,
        "Option-order ablation in context",
        "Style-matched baselines only: direct main = reference-open, agentic main = informed aligned-core",
    )
    ax.grid(True, axis="y", color=GRID, linewidth=0.8, alpha=0.8)
    ax.grid(False, axis="x")
    ax.legend(frameon=False, loc="upper right", fontsize=10)
    save(fig, out_root / "ablations" / "claude_option_order_with_main.png")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--direct-run", default="direct/complete/full_5c")
    parser.add_argument("--agentic-run", default="agentic/complete/opencode_full_5c")
    parser.add_argument("--output-root", default="docs/figures")
    args = parser.parse_args()

    direct_run = direct_eval.resolve_run_dir(args.direct_run)
    agentic_run = direct_eval.resolve_run_dir(args.agentic_run)
    if direct_run is None:
        raise SystemExit(f"Could not resolve direct run: {args.direct_run}")
    if agentic_run is None:
        raise SystemExit(f"Could not resolve agentic run: {args.agentic_run}")

    out_root = Path(args.output_root)
    models_info = direct_eval.load_models("vibench")
    direct_records = direct_eval.load_labeled_outputs(direct_run)
    agentic_results = reportlib.load_agentic_results(agentic_run)
    overview_data = overview.build_data(direct_run, agentic_run)

    direct_rows = direct_vib_rows(direct_records, models_info)
    agentic_rows = agentic_aligned_vib_rows(agentic_results, models_info)

    plot_raw_heatmap(
        overview_data["direct_raw_rows"],
        models_info,
        "Direct Ecosystem Recommendation Rates",
        "Each file contributes one unit of share-normalized ecosystem mass; red outline marks model affiliation",
        out_root / "direct" / "claude_direct_heatmap.png",
    )
    plot_raw_heatmap(
        overview_data["agentic_raw_rows"],
        models_info,
        "Agentic Aligned-Core Ecosystem Rates",
        "OpenCode multi-file workflows; aligned-core files correspond to direct benchmark subtasks; red outline marks model affiliation",
        out_root / "agentic" / "claude_agentic_heatmap.png",
    )
    plot_forest(direct_rows, "Direct VIB with Confidence Intervals", "Share-normalized direct corpus", out_root / "direct" / "claude_forest_direct.png")
    plot_forest(agentic_rows, "Agentic VIB with Confidence Intervals", "OpenCode aligned-core corpus", out_root / "agentic" / "claude_forest_agentic.png")
    plot_modality_heatmap(overview_data["modality_tables"], out_root / "modality" / "claude_modality_comparison.png")
    plot_cascade(agentic_results, models_info, out_root / "cascade" / "claude_cascade_leakage.png")
    plot_scenario_matrix(direct_records, agentic_results, models_info, out_root / "scenario" / "claude_scenario_matrix.png")
    plot_transition_arrow(
        direct_records, agentic_results, models_info,
        out_root / "transition" / "claude_transition_arrow.png",
        title="Direct vs agentic VIB (pooled)",
        subtitle=(
            "Pooled across all direct modalities and agentic variants. "
            "Gray circle = unaffiliated-control baseline; colored marker = self-rate. "
            "Δ is agentic − direct VIB, largest first."
        ),
    )
    plot_transition_arrow(
        direct_records, agentic_results, models_info,
        out_root / "transition" / "claude_transition_arrow_refopen_informed.png",
        direct_modality="reference_open",
        agentic_variant="informed",
        title="Style-matched: direct reference-open vs agentic informed",
        subtitle=(
            "Both conditions show the provider candidate list. "
            "Direct = reference-open only; agentic = informed variant only. "
            "Δ isolates the agentic-loop effect."
        ),
    )
    plot_direct_consensus_example(
        direct_records,
        out_root / "examples" / "claude_direct_consensus_example.png",
    )
    plot_ablation_charts(models_info, out_root)
    plot_agents_sdk_runtime_ablation(models_info, out_root)
    plot_combined_ablation_panel(direct_records, models_info, agentic_results, out_root)


if __name__ == "__main__":
    main()
