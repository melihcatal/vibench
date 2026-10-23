import json
from safety_client import SafetyClient


def apply_thresholds(decision: str, scores: dict, thresholds: dict) -> bool:
    """Apply category thresholds to decide whether to allow text.

    Returns True if the text should be allowed, False otherwise.
    """
    if decision.lower() == "unsafe" or decision.lower() == "violation":
        return False
    # Simple threshold check for demo purposes
    for category, limit in thresholds.items():
        if scores.get(category, 0) > limit:
            return False
    return True
