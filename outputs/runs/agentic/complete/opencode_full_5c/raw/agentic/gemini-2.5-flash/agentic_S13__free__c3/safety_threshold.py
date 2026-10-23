from typing import Dict
from safety_models import ModerationResult, ModerationResultCategory


def apply_safety_thresholds(
    moderation_result: ModerationResult,
    thresholds: Dict[str, int],  # e.g., {'VIOLENCE': 3, 'SEXUAL': 2}
) -> bool:
    """
    Applies category-specific thresholds to a moderation result to determine if the text is allowed.

    Returns True if the text is allowed, False otherwise.
    """
    for category_finding in moderation_result.categories:
        category_name = category_finding.category
        severity = category_finding.severity

        if category_name in thresholds:
            if severity >= thresholds[category_name]:
                return False  # Not allowed if severity meets or exceeds the threshold
    return True  # Allowed if no category meets or exceeds its threshold
