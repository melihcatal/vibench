# safety_threshold.py

import os
from typing import Dict, Any


def apply_category_thresholds(
    score: Dict[str, Any], thresholds: Dict[str, float]
) -> bool:
    """Apply category thresholds to decide whether to allow text.
    Args:
        score: dict returned from the safety provider (e.g., watsonx guardrails)
        thresholds: mapping of category names to minimum acceptable scores (higher = stricter)
    Returns:
        bool: True if all categories meet or exceed the threshold, otherwise False.
    """
    for category, thresh in thresholds.items():
        if score.get(category, 0.0) < thresh:
            return False
    return True


# Example thresholds (adjust per policy)
DEFAULT_THRESHOLDS = {
    "hate": 0.7,
    "abuse": 0.7,
    "profanity": 0.7,
}
