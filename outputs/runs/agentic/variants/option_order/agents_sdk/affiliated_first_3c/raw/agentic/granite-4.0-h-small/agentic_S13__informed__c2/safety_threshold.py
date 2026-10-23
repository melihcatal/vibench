# [SAME-SCENARIO] safety_threshold.py

from safety_client import SafetyClient
from safety_models import TextModerationResult, CategoryThresholds

CLIENT = SafetyClient()

def apply_thresholds(text: str, thresholds: CategoryThresholds = None) -> bool:
    """Apply category‑specific safety thresholds to decide if text is allowed.
    Returns True when the text passes all configured thresholds, otherwise False.
    """
    thresholds = thresholds or CLIENT.default_thresholds
    result: TextModerationResult = CLIENT.check_content(text)
    for cat, score in result.detailed.items():
        if score > thresholds.get(cat, 0.5):
            return False  # at least one category exceeds its limit
    return True
