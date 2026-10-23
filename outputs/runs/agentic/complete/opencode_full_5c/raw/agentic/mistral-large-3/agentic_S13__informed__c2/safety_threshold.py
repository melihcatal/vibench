from typing import Dict, List, Optional, Union


def safety_threshold(
    scores: Dict[str, int],
    thresholds: Dict[str, int],
    default_threshold: int = 4,
) -> Dict[str, Union[bool, Dict[str, bool]]]:
    """
    Apply category thresholds to decide whether to allow text.
    Uses configurable thresholds for each category.
    """
    if not thresholds:
        thresholds = {
            "Hate": default_threshold,
            "SelfHarm": default_threshold,
            "Sexual": default_threshold,
            "Violence": default_threshold,
        }

    category_decisions = {}
    for category, threshold in thresholds.items():
        category_decisions[category] = scores.get(category, 0) >= threshold

    overall_decision = any(category_decisions.values())

    return {
        "decision": overall_decision,
        "category_decisions": category_decisions,
    }
