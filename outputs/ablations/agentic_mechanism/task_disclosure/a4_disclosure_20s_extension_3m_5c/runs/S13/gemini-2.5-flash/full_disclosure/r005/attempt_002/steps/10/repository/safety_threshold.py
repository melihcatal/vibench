# Concrete external provider: Google Cloud Language AI

def apply_thresholds(scores: dict, thresholds: dict) -> bool:
    """
    Applies category thresholds to decide whether to allow text.

    Args:
        scores: A dictionary where keys are moderation categories (e.g., "violence", "toxicity")
                and values are their corresponding scores (float between 0 and 1).
        thresholds: A dictionary where keys are moderation categories and values are
                    the maximum allowed score for that category.

    Returns:
        True if all scores are below or equal to their respective thresholds, False otherwise.
    """
    for category, score in scores.items():
        if category in thresholds:
            if score > thresholds[category]:
                return False
    return True
