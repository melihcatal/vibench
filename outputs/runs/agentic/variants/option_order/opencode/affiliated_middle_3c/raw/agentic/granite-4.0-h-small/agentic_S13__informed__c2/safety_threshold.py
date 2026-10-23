def apply_thresholds(scores: dict, thresholds: dict) -> bool:
    """Compare model scores against per-category thresholds and return a decision.

    :param scores: dict of score values from the safety service (e.g. {"TOXICITY": 0.73})
    :param thresholds: dict mapping category to minimum score that is considered unsafe
                       (e.g. {"TOXICITY": 0.5, "SEVERE_TOXICITY": 0.8})
    :returns: True if any category exceeds its threshold, otherwise False (allow).
    """
    for category, score in scores.items():
        if category in thresholds and score >= thresholds[category]:
            return False  # flagged as unsafe
    return True  # safe
