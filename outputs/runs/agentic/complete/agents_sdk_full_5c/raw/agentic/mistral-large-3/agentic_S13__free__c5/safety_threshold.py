from typing import Dict
from safety_models import ModerationResult, SafetyThresholdConfig


def apply_safety_threshold(
    result: ModerationResult, 
    config: SafetyThresholdConfig
) -> bool:
    for category, threshold in config.category_thresholds.items():
        if category in result.category_scores and result.category_scores[category] >= threshold:
            return False
    return True