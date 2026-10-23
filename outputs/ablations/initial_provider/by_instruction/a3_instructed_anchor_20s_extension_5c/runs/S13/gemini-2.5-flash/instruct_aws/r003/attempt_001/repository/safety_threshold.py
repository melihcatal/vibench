from safety_models import TextModerationResponse, ThresholdConfig, ThresholdDecision
from typing import Dict, Any

def apply_safety_thresholds(moderation_response: TextModerationResponse, config: ThresholdConfig) -> ThresholdDecision:
    is_allowed = True
    decision_details: Dict[str, Any] = {}

    for category, score in moderation_response.categories.items():
        threshold = config.thresholds.get(category, config.decision_threshold)
        if score >= threshold:
            is_allowed = False
            decision_details[category] = {"score": score, "threshold": threshold, "exceeded": True}
        else:
            decision_details[category] = {"score": score, "threshold": threshold, "exceeded": False}

    if moderation_response.is_unsafe:
        is_allowed = False
        decision_details["overall_unsafe_flag"] = {"is_unsafe_flagged": True}

    return ThresholdDecision(is_allowed=is_allowed, decision_details=decision_details)
