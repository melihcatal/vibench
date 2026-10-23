from safety_models import SafetyThresholdRequest, MessageDecision
from typing import List


def safety_threshold(payload: SafetyThresholdRequest) -> MessageDecision:
    moderation_result = payload.moderation_result
    threshold_configs = payload.threshold_configs

    decision = "allow"
    reasons: List[str] = []

    for category_analysis in moderation_result.categories:
        for threshold_config in threshold_configs:
            if category_analysis.category == threshold_config.category and category_analysis.severity >= threshold_config.threshold:
                decision = threshold_config.action
                reasons.append(f"{category_analysis.category} exceeded threshold (severity: {category_analysis.severity}, threshold: {threshold_config.threshold})")
                if decision == "block":
                    break
        if decision == "block":
            break

    return MessageDecision(text=moderation_result.text, decision=decision, reasons=reasons)
