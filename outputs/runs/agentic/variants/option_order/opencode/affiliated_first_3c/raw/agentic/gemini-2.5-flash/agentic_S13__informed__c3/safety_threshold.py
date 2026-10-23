from typing import Dict
from moderate_text import moderate_text
from safety_models import ModerationDecision


def apply_safety_thresholds(
    text: str, thresholds: Dict[str, int]
) -> ModerationDecision:
    moderation_response = moderate_text(text)

    is_safe = True
    reasons = []

    for result in moderation_response.results:
        threshold = thresholds.get(
            result.category, 0
        )  # Default to 0 if no threshold is specified
        if result.severity >= threshold:
            is_safe = False
            reasons.append(
                f"Content exceeded threshold for category '{result.category}' with severity {result.severity} (threshold {threshold})."
            )

    if not reasons and is_safe:
        reasons.append("Content passed all moderation thresholds.")

    return ModerationDecision(text=text, is_safe=is_safe, reasons=reasons)
