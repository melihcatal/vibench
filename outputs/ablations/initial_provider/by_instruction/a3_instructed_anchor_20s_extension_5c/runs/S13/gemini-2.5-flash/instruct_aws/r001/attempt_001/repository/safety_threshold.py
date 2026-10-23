from safety_models import TextModerationResponse, ThresholdConfig
from typing import List

def apply_safety_thresholds(response: TextModerationResponse, thresholds: List[ThresholdConfig]) -> bool:
    """
    Applies safety thresholds to a moderation response to determine if the text is allowed.
    Returns True if allowed, False otherwise.
    """
    for threshold_config in thresholds:
        category = threshold_config.category
        threshold = threshold_config.threshold

        if category in response.scores and response.scores[category] > threshold:
            return False  # Not allowed if any category exceeds its threshold
    return True  # Allowed if no category exceeds its threshold
