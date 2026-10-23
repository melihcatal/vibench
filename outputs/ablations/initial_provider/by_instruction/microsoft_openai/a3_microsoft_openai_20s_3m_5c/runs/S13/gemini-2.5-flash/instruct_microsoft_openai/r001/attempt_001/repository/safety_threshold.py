from typing import List
from safety_models import ModerationResponse, ThresholdConfig, TextDecision

def apply_safety_thresholds(moderation_response: ModerationResponse, thresholds: List[ThresholdConfig], original_text: str) -> TextDecision:
    """
    Applies category thresholds to decide whether to allow text based on moderation results.
    """
    decision = "allow"
    reasons = []

    for threshold_config in thresholds:
        category = threshold_config.category
        threshold_value = threshold_config.threshold
        action = threshold_config.action

        if category in moderation_response.category_scores:
            score = moderation_response.category_scores[category]
            if score > threshold_value:
                if action == "block":
                    decision = "block"
                    reasons.append(f"Blocked due to high score in category '{category}' (score: {score:.2f} > threshold: {threshold_value:.2f})")
                    break # Highest severity action, no need to check further
                elif action == "flag" and decision != "block":
                    decision = "flag"
                    reasons.append(f"Flagged due to score in category '{category}' (score: {score:.2f} > threshold: {threshold_value:.2f})")

    if not reasons and moderation_response.flagged and decision == "allow":
        decision = "flag"
        reasons.append("Flagged by general moderation model despite no specific threshold breach.")

    return TextDecision(
        text=original_text,
        decision=decision,
        reasons=reasons
    )
