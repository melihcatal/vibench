from __future__ import annotations

from typing import Dict, Optional

from safety_client import get_category_thresholds
from safety_models import ModerationDecision, ThresholdDecision, category_score_map


def apply_safety_threshold(decision: ModerationDecision, thresholds: Optional[Dict[str, float]] = None) -> ThresholdDecision:
    configured = thresholds or get_category_thresholds()
    observed = category_score_map(decision.categories)
    blocked = sorted(
        category
        for category, score in observed.items()
        if score >= configured.get(category, 1.1)
    )
    return ThresholdDecision(
        allowed=not blocked,
        blocked_categories=blocked,
        observed_scores=observed,
    )
