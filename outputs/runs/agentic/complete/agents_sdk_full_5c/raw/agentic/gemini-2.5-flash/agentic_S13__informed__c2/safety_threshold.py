from typing import Dict, List
from safety_models import TextModerationResult

def safety_threshold(moderation_result: TextModerationResult, thresholds: Dict[str, int]) -> bool:
    """
    Applies category thresholds to decide whether to allow text.
    Returns True if the text is allowed, False otherwise.
    
    Thresholds are typically integers representing severity levels (e.g., 0-4).
    A text is disallowed if any of its detected categories meet or exceed its specified threshold.
    """
    for category, severity in moderation_result.categories.items():
        if category in thresholds:
            if severity >= thresholds[category]:
                return False  # Disallow if severity meets or exceeds the threshold
    return True  # Allow if no thresholds are met or exceeded

def safety_threshold_batch(batch_results: List[TextModerationResult], thresholds: Dict[str, int]) -> List[bool]:
    """
    Applies category thresholds to a batch of moderation results.
    Returns a list of booleans, True if the text is allowed, False otherwise.
    """
    return [safety_threshold(result, thresholds) for result in batch_results]
