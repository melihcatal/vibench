from typing import Dict, Any
from safety_models import TextModerationResponse, ModerationCategory


def apply_safety_thresholds(
    response: TextModerationResponse, thresholds: Dict[ModerationCategory, float]
) -> bool:
    """
    Applies category thresholds to decide whether to allow text.
    Returns True if the text is allowed (i.e., no category exceeds its threshold), False otherwise.
    """
    for category, threshold in thresholds.items():
        if response.is_unsafe(category, threshold):
            return False
    return True
