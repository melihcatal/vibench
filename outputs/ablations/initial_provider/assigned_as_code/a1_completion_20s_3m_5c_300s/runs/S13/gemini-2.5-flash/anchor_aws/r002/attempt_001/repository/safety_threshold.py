from typing import Dict, Any
from safety_models import ModerationResult

def safety_threshold(moderation_result: ModerationResult, thresholds: Dict[str, float]) -> ModerationResult:
    for category, score in moderation_result.categories.items():
        if category in thresholds and score > thresholds[category]:
            moderation_result.decision = "deny"
            return moderation_result
    moderation_result.decision = "allow"
    return moderation_result
