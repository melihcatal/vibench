from typing import Dict
from safety_models import ModerationResult, ModerationDecision


def apply_safety_thresholds(
    result: ModerationResult, thresholds: Dict[str, int]
) -> ModerationDecision:
    decision = "allow"
    reasons = []

    for category_detection in result.categories_detection:
        category = category_detection.category
        severity = category_detection.severity

        if category in thresholds and severity > thresholds[category]:
            decision = "deny"
            reasons.append(
                f"Content denied due to {category} exceeding severity threshold ({severity} > {thresholds[category]})."
            )

    if not reasons and result.is_unsafe:
        # If no specific threshold was exceeded but the general 'is_unsafe' flag is true
        # this could mean default unsafe behavior or a category not explicitly in thresholds.
        decision = "deny"
        reasons.append("Content denied due to general unsafe content detection.")

    return ModerationDecision(text=result.text, decision=decision, reasons=reasons)
