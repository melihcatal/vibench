from safety_models import severity_to_score, ModerationResult

def apply_safety_threshold(result: ModerationResult, category_thresholds: dict[str, str]) -> bool:
    """
    Returns True if text is allowed, False if blocked.
    """
    for category, threshold in category_thresholds.items():
        result_severity = result.categories.get(category, "none")
        if severity_to_score(result_severity) > severity_to_score(threshold):
            return False
    return True
