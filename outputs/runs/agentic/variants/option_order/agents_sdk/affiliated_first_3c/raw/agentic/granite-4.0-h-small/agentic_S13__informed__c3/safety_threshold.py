import os

def apply_thresholds(categories: dict, thresholds: dict) -> bool:
    """Apply per-category thresholds to decide whether text passes moderation.
    Returns True if all category scores are below their respective thresholds, else False.
    """
    for cat, score in categories.items():
        if cat in thresholds and score > thresholds[cat]:
            return False
    return True

# Example default thresholds (can be overridden per deployment)
DEFAULT_THRESHOLDS = {
    'hate': 0.5,
    'self_harm': 0.5,
    'sexual': 0.5,
    'violence': 0.5,
    # add other categories as needed
}
