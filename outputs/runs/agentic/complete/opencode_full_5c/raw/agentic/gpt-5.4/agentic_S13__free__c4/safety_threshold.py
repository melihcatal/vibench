from __future__ import annotations

from safety_client import moderation_thresholds
from safety_models import ThresholdDecision, summarize_triggered_categories


def apply_safety_threshold(
    category_scores: dict[str, float], thresholds: dict[str, float] | None = None
) -> ThresholdDecision:
    active_thresholds = thresholds or moderation_thresholds()
    triggered = summarize_triggered_categories(category_scores, active_thresholds)
    return ThresholdDecision(
        allow=not triggered,
        triggered_categories=triggered,
        scores=dict(category_scores),
    )
