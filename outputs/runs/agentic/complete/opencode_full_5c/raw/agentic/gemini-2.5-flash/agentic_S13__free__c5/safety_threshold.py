from typing import List
from safety_models import ModerationResponse, TextSafetyDecision, ModerationCategory


def apply_safety_thresholds(
    original_text: str, moderation_response: ModerationResponse, thresholds: dict
) -> TextSafetyDecision:
    allowed = True
    reasons = []

    for category_score in moderation_response.categories:
        threshold = thresholds.get(category_score.name)
        if threshold is not None and category_score.score > threshold:
            allowed = False
            reasons.append(
                f"Category '{category_score.name}' score ({category_score.score}) exceeded threshold ({threshold})"
            )

    if not reasons and not moderation_response.is_unsafe:
        pass  # If no specific category exceeded threshold, and not generally unsafe, then it's allowed.
    elif (
        not reasons and moderation_response.is_unsafe
    ):  # If generally unsafe but no specific category exceeded threshold based on provided thresholds.
        allowed = False
        reasons.append("Text generally deemed unsafe by moderation service.")

    if not reasons and allowed:
        reasons.append("Text passed all safety thresholds.")

    return TextSafetyDecision(text=original_text, allowed=allowed, reasons=reasons)
