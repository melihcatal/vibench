from safety_models import TextModerationResult
from typing import Dict


def apply_safety_threshold(
    result: TextModerationResult, thresholds: Dict[str, float]
) -> Dict[str, bool]:
    """
    Applies category thresholds to decide whether to allow text.
    Returns a dictionary indicating if the text is allowed for each category.
    """
    decisions = {}
    for category_analysis in result.categories_analysis:
        category = category_analysis["category"]
        severity = category_analysis.get("severity", 0)

        threshold = thresholds.get(category, 0.0)  # Default threshold if not specified

        is_allowed = severity < threshold
        decisions[category] = is_allowed

    return decisions
