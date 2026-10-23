from typing import Dict
from safety_models import TextModerationResponse


def apply_safety_thresholds(
    moderation_response: TextModerationResponse, thresholds: Dict[str, int]
) -> str:
    """
    Applies category thresholds to decide whether to allow text.
    Returns "Allow" if all categories are below their thresholds, otherwise "Deny".
    """
    for result in moderation_response.results:
        category = result.category
        severity = result.severity

        if category in thresholds and severity >= thresholds[category]:
            return "Deny"

    return "Allow"
