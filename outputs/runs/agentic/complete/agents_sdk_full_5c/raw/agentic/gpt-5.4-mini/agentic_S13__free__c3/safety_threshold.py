from typing import Dict

from safety_client import configure_client
from safety_models import ModerationDecision, SafetyThresholds

DEFAULT_THRESHOLDS = SafetyThresholds(
    thresholds={
        "harassment": 0.7,
        "hate": 0.6,
        "self_harm": 0.5,
        "sexual": 0.7,
        "violence": 0.7,
        "illegal": 0.6,
        "spam": 0.8,
    }
)


def apply_thresholds(decision: ModerationDecision, thresholds: Dict[str, float] | None = None) -> bool:
    configure_client()
    active = thresholds or DEFAULT_THRESHOLDS.thresholds
    for category, score in decision.categories.items():
        if score >= active.get(category, 1.0):
            return False
    return decision.allow
