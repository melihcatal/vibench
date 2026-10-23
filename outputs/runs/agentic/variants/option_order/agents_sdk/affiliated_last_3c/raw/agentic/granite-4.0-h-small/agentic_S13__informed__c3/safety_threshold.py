def apply_category_thresholds(scores: dict, thresholds: dict = None) -> dict:
    """Apply category thresholds to decide whether text is allowed.

    Args:
        scores: dict of category names to numeric scores (e.g., {'TOXICITY': 0.73})
        thresholds: optional dict mapping category to threshold value.
    Returns:
        dict with original scores and an 'allowed' boolean based on thresholds.
    """
    applied = scores.copy()
    allowed = True
    if thresholds is None:
        thresholds = {}  # default no threshold enforcement
    for cat, score in scores.items():
        thr = thresholds.get(cat, 0.5)
        applied[f"{cat}_exceeds"] = score >= thr
        if score >= thr:
            allowed = False
    applied["allowed"] = allowed
    return applied
