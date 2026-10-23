from typing import Dict, List
from safety_models import SafetyCategory, ModerationResult


def apply_safety_threshold(
    result: ModerationResult, thresholds: Dict[SafetyCategory, float]
) -> bool:
    """
    Applies category thresholds to decide whether to allow text using Google Cloud Natural Language API results.
    Model: google/cloud-language-v1
    """
    for category in result["categories"]:
        if result["confidence"] >= thresholds.get(category, 0.5):
            return False
    return True
