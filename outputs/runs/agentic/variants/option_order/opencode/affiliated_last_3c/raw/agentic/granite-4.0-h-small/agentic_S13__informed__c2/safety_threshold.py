# safety_threshold.py
# SAME-SCENARIO implementation
# Applies category thresholds to decide whether to allow user text

import os


def apply_threshold(moderation_response: dict, thresholds: dict) -> bool:
    """Check moderation response against per-category thresholds.

    Returns True if text passes all thresholds, False otherwise.
    """
    # Example thresholds: {'abuse': 0.7, 'personal_data': 0.5}
    for category, max_score in thresholds.items():
        # Assume provider returns a 'scores' dict with numeric confidence per category
        if category in moderation_response.get("scores", {}):
            if moderation_response["scores"][category] > max_score:
                return False
    return True


# Example usage (not executed)
# thresholds = {'abuse': 0.75, 'self_harm': 0.6}
# if apply_threshold(moderation_response, thresholds):
#     allow_text()
