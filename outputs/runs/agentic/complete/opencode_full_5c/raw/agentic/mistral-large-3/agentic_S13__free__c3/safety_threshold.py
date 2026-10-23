from typing import Dict, List, Optional
from safety_client import TextModerator
from safety_models import normalize_response


def apply_safety_threshold(
    text: str, thresholds: Dict[str, int] = None, categories: Optional[List[str]] = None
) -> Dict:
    """
    Applies category thresholds to decide whether to allow text using Azure Content Safety.
    Model: 2024-02-15-preview
    """
    if thresholds is None:
        thresholds = {"Hate": 2, "SelfHarm": 2, "Sexual": 2, "Violence": 2}

    moderator = TextModerator()
    response = moderator.moderate_text(text, categories)
    normalized = normalize_response(response)

    if normalized.error:
        return {
            "allowed": False,
            "reason": normalized.error,
            "categories_triggered": [],
        }

    categories_triggered = []
    for analysis in normalized.categories_analysis:
        if analysis.severity >= thresholds.get(analysis.category, 0):
            categories_triggered.append(analysis.category)

    return {
        "allowed": len(categories_triggered) == 0,
        "reason": "Threshold exceeded" if categories_triggered else "Allowed",
        "categories_triggered": categories_triggered,
    }
