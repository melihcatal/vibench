from typing import Dict
from safety_models import ModerationResult, ModerationCategory


def apply_safety_thresholds(
    result: ModerationResult, thresholds: Dict[str, int]
) -> bool:
    """
    Applies category-specific thresholds to a moderation result to determine if the text is allowed.
    Returns True if the text is allowed, False otherwise.
    """
    for category_result in result.categories:
        if category_result.category in thresholds:
            if category_result.severity >= thresholds[category_result.category]:
                return False  # Block if severity meets or exceeds the threshold for this category
    return True  # Allow if no category exceeds its threshold
