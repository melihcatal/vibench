from typing import Dict
from safety_models import ModerationResult

def is_text_allowed(result: ModerationResult, thresholds: Dict[str, int]) -> bool:
    """
    Applies category severity thresholds to decide whether to allow text.

    Args:
        result: The moderation result for a piece of text.
        thresholds: A dictionary mapping category names to max allowed severity.
                    Example: {'Hate': 2, 'SelfHarm': 4}
                    Azure Content Safety severities are 0, 2, 4, 6.
                    A threshold of 2 means severities 4 and 6 will be blocked.

    Returns:
        True if the text is allowed, False otherwise.
    """
    for category_result in result.categories:
        category_name = category_result.category
        severity = category_result.severity

        if category_name in thresholds:
            # If the severity is greater than the allowed threshold, block it.
            if severity > thresholds[category_name]:
                return False
    
    return True
