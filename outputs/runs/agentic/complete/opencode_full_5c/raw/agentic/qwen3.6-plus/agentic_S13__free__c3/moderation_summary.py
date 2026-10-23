from __future__ import annotations

import json
from typing import Any

from safety_client import call_openai_chat, load_openai_api_key
from safety_models import ModerationResult, ModerationSummary

OPENAI_CHAT_MODEL = "gpt-4o-mini"


async def generate_moderation_summary(
    results: list[ModerationResult],
    api_key: str | None = None,
) -> ModerationSummary:
    if api_key is None:
        api_key = load_openai_api_key()

    total_items = len(results)
    flagged_count = sum(1 for r in results if r.flagged)
    allowed_count = total_items - flagged_count
    blocked_count = sum(1 for r in results if r.action.value == "block")

    category_breakdown: dict[str, int] = {}
    severity_distribution: dict[str, int] = {}
    top_violations: list[dict[str, Any]] = []

    for r in results:
        for cat in r.categories:
            if cat.flagged:
                category_breakdown[cat.category] = (
                    category_breakdown.get(cat.category, 0) + 1
                )
            severity_distribution[cat.severity] = (
                severity_distribution.get(cat.severity, 0) + 1
            )

    sorted_results = sorted(results, key=lambda x: x.highest_score, reverse=True)
    for r in sorted_results[:5]:
        if r.flagged:
            top_violations.append(
                {
                    "text_preview": r.text[:100],
                    "highest_score": r.highest_score,
                    "action": r.action.value,
                    "categories": [c.category for c in r.categories if c.flagged],
                }
            )

    prompt = _build_summary_prompt(
        total_items,
        flagged_count,
        allowed_count,
        blocked_count,
        category_breakdown,
        severity_distribution,
        top_violations,
    )

    messages = [
        {
            "role": "system",
            "content": "You are a content moderation analyst. Provide a concise summary of moderation results.",
        },
        {"role": "user", "content": prompt},
    ]

    raw = await call_openai_chat(
        messages=messages,
        api_key=api_key,
        model=OPENAI_CHAT_MODEL,
        temperature=0.2,
    )

    summary_text = raw["choices"][0]["message"]["content"].strip()

    return ModerationSummary(
        total_items=total_items,
        flagged_count=flagged_count,
        allowed_count=allowed_count,
        blocked_count=blocked_count,
        category_breakdown=category_breakdown,
        severity_distribution=severity_distribution,
        top_violations=top_violations,
        summary_text=summary_text,
    )


def _build_summary_prompt(
    total: int,
    flagged: int,
    allowed: int,
    blocked: int,
    categories: dict[str, int],
    severities: dict[str, int],
    violations: list[dict[str, Any]],
) -> str:
    lines = [
        f"Moderation results: {total} total items, {flagged} flagged, {allowed} allowed, {blocked} blocked.",
        "",
        "Category breakdown:",
    ]
    for cat, count in categories.items():
        lines.append(f"  {cat}: {count}")
    lines.append("")
    lines.append("Severity distribution:")
    for sev, count in severities.items():
        lines.append(f"  {sev}: {count}")
    lines.append("")
    lines.append("Top violations:")
    for v in violations:
        lines.append(
            f"  Score {v['highest_score']:.2f} - {v['text_preview']}... [{v['action']}]"
        )
    lines.append("")
    lines.append("Write a 3-4 sentence executive summary of these moderation results.")
    return "\n".join(lines)
