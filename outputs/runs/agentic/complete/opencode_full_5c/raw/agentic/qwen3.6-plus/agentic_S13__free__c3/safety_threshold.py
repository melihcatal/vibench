from __future__ import annotations

from typing import Any

from safety_client import call_perspective_api, load_perspective_api_key
from safety_models import (
    CategoryScore,
    ModerationAction,
    ThresholdDecision,
    normalize_perspective_categories,
)

DEFAULT_THRESHOLDS: dict[str, float] = {
    "TOXICITY": 0.7,
    "SEVERE_TOXICITY": 0.5,
    "IDENTITY_ATTACK": 0.6,
    "INSULT": 0.65,
    "PROFANITY": 0.75,
    "THREAT": 0.4,
}

PERSPECTIVE_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
]


async def apply_safety_threshold(
    text: str,
    thresholds: dict[str, float] | None = None,
    api_key: str | None = None,
) -> ThresholdDecision:
    if api_key is None:
        api_key = load_perspective_api_key()
    if thresholds is None:
        thresholds = dict(DEFAULT_THRESHOLDS)

    raw = await call_perspective_api(
        text=text,
        api_key=api_key,
        attributes=PERSPECTIVE_ATTRIBUTES,
        languages=["en"],
    )

    attribute_scores = raw.get("attributeScores", {})
    raw_scores: dict[str, float] = {}
    for attr_name, attr_data in attribute_scores.items():
        summary_score = attr_data.get("summaryScore", {})
        raw_scores[attr_name] = summary_score.get("value", 0.0)

    category_scores = normalize_perspective_categories(raw_scores)

    exceeded_categories: list[str] = []
    for cat in category_scores:
        threshold = thresholds.get(cat.category, 0.5)
        if cat.score >= threshold:
            exceeded_categories.append(cat.category)

    allowed = len(exceeded_categories) == 0
    rationale = _build_rationale(allowed, exceeded_categories, raw_scores, thresholds)

    return ThresholdDecision(
        text=text,
        allowed=allowed,
        category_scores=category_scores,
        threshold_applied=thresholds,
        exceeded_categories=exceeded_categories,
        rationale=rationale,
    )


def _build_rationale(
    allowed: bool,
    exceeded: list[str],
    scores: dict[str, float],
    thresholds: dict[str, float],
) -> str:
    if allowed:
        return "All category scores are within acceptable thresholds."
    parts = []
    parts.append("Text blocked due to exceeded thresholds:")
    for cat in exceeded:
        score = scores.get(cat, 0.0)
        thresh = thresholds.get(cat, 0.5)
        parts.append(f"  {cat}: {score:.3f} (threshold: {thresh:.3f})")
    return "\n".join(parts)
