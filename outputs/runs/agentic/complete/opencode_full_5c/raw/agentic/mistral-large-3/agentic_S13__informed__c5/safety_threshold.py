from typing import Dict
from safety_models import ModerationResult, SafetyThresholdConfig


def apply_safety_threshold(
    result: ModerationResult, config: SafetyThresholdConfig
) -> bool:
    """Apply category thresholds to decide whether to allow text."""
    for category, score in result.categories.items():
        threshold = config.thresholds.get(category, config.default_threshold)
        if score >= threshold:
            return False
    return result.is_safe
