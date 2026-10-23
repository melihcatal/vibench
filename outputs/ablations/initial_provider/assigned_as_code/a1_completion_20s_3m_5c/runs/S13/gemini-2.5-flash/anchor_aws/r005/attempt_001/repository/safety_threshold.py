from typing import Dict, Any, List
from safety_models import TextModerationResponse, ModerationCategory

def apply_safety_thresholds(moderation_results: Dict[str, Any], thresholds: Dict[str, float]) -> Dict[str, Any]:
    """
    Applies category thresholds to moderation results to determine if text is allowed.

    Args:
        moderation_results: A dictionary containing moderation scores, e.g., from moderate_text.py.
                            Expected format: {"toxicity": 0.75, ...}
        thresholds: A dictionary mapping moderation categories (as strings) to their float thresholds.
                    Example: {"TOXICITY": 0.6}

    Returns:
        A dictionary with a boolean 'allowed' indicating if the text passes all thresholds
        and a list of 'violations' for categories that exceeded their threshold.
    """
    allowed = True
    violations = []

    # Assuming moderation_results format is like {"toxicity": 0.75}
    # and thresholds format is {"TOXICITY": 0.6}

    # Convert keys to uppercase to match ModerationCategory enum if necessary
    normalized_thresholds = {k.upper(): v for k, v in thresholds.items()}

    for category_str, score in moderation_results.items():
        category = ModerationCategory[category_str.upper()] # Convert string to enum
        if category.value in normalized_thresholds:
            if score > normalized_thresholds[category.value]:
                allowed = False
                violations.append({"category": category.value, "score": score, "threshold": normalized_thresholds[category.value]})

    return {"allowed": allowed, "violations": violations}
