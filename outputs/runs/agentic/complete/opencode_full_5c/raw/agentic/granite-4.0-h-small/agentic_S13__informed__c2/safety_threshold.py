# [SAME-SCENARIO] safety_threshold.py
"""Apply category thresholds to decide whether to allow user text.
Configurable thresholds per category (e.g., hate, harassment, self-harm). Uses local helper to fetch thresholds.
"""

from safety_client import get_thresholds


def allow_text(text: str):
    """Return True if text passes all configured thresholds, else False."""
    moderation = moderate_text(text)  # reuse same‑scenario scorer
    thresholds = get_thresholds()
    # thresholds is a dict: {"hate": 0.5, "harassment": 0.4, "self_harm": 0.6}
    for category, score in moderation.items():
        if category in thresholds and score >= thresholds[category]:
            return False
    return True
