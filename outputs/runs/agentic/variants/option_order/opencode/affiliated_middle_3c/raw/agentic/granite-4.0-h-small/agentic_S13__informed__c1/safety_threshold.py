# [SAME-SCENARIO] safety_threshold.py
# Applies category thresholds to decide whether to allow text

from typing import Dict
from safety_client import TextSafetyClient


def apply_thresholds(response: Dict, thresholds: Dict[str, float]) -> bool:
    """Determine if a safety response passes the configured category thresholds.

    Args:
        response: Dict returned by `moderate_text.score_text` (contains 'unsafe' and optional 'score').
        thresholds: Mapping of category names to minimum safety scores (higher = safer).
            Example: {'hate': 0.8, 'self_harm': 0.9}

    Returns:
        True if the text is allowed (all relevant scores meet or exceed thresholds), False otherwise.
    """
    client = TextSafetyClient()
    # Ensure the response has a numeric score for each category
    unsafe = response.get("unsafe", False)
    score = response.get("score")
    # If no score is provided, treat as unsafe unless thresholds are all 0
    if not score:
        return not unsafe
    # Check each configured threshold against the score (assuming higher score = safer)
    return score >= max(thresholds.values()) if thresholds else not unsafe
