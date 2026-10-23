def apply_threshold(labels: dict, thresholds: dict) -> bool:
    """Decide whether text passes safety thresholds.

    labels: dict mapping label names to severity scores (0-1).
    thresholds: dict mapping label names to maximum allowed scores.
    Returns True if all scores are <= corresponding thresholds, else False.
    """
    for label, score in labels.items():
        if score > thresholds.get(label, 1.0):
            return False
    return True
