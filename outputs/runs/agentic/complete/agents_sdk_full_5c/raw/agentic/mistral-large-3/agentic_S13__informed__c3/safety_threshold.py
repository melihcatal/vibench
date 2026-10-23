from typing import Dict, List
from safety_models import SafetyCategory, TextModerationResponse


def apply_thresholds(
    response: TextModerationResponse,
    thresholds: Dict[SafetyCategory, float]
) -> bool:
    """
    Apply category thresholds to decide whether to allow text.
    Returns True if text is allowed, False if blocked.
    """
    for score in response.scores:
        threshold = thresholds.get(score["category"], 0.5)
        if score["score"] > threshold:
            return False
    return True