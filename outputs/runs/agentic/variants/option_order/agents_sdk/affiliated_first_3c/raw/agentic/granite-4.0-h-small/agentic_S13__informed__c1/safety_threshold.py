# [SAME-SCENARIO] safety_threshold.py

from safety_models import SafetyResponse

# Simple category‑wise thresholds for allowing text
THRESHOLDS = {
    "harassment": 0.3,
    "hate": 0.2,
    "self_harm": 0.1,
    "sexual": 0.15,
    "violence": 0.25,
}

def safety_threshold(response: SafetyResponse) -> bool:
    """Decides whether the input text passes the configured safety thresholds.

    Returns True if all category scores are below their thresholds, otherwise False.
    """
    for category, score in response.category_scores.items():
        if category in THRESHOLDS and score >= THRESHOLDS[category]:
            return False
    return True
