# Applies category thresholds to decide whether to allow text
from typing import Dict
from safety_models import SafetyCategory, SafetyDecision
from safety_client import get_default_thresholds


def apply_thresholds(scores: Dict[SafetyCategory, float]) -> SafetyDecision:
    """Apply category thresholds to moderation scores."""
    thresholds = get_default_thresholds()
    blocked_reason = None

    for category, score in scores.items():
        if score >= thresholds[category.value]:
            blocked_reason = f"high {category.value} score"
            break

    decision = SafetyDecision(
        allowed=blocked_reason is None,
        categories=scores,
        blocked_reason=blocked_reason
    )
    return decision