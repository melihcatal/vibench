from safety_models import TextModerationResponse, ModerationDecision
from typing import Dict


def apply_safety_thresholds(
    moderation_response: TextModerationResponse, thresholds: Dict[str, float]
) -> ModerationDecision:
    is_safe = True
    reasons = []

    for category, score in moderation_response.category_scores.items():
        if category in thresholds and score >= thresholds[category]:
            is_safe = False
            reasons.append(
                f"Category '{category}' exceeded threshold with score {score:.2f}"
            )

    if not is_safe:
        suggested_action = "Reject"
    else:
        suggested_action = "Accept"

    return ModerationDecision(
        text="",  # The original text is not part of this decision, but would be passed in a real scenario
        is_safe=is_safe,
        reasons=reasons,
        category_scores=moderation_response.category_scores,
    )
