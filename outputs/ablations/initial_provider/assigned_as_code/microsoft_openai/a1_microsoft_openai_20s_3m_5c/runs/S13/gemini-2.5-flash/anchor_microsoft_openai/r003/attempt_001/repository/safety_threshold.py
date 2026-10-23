from safety_models import ModerationResult, TextCategories

def apply_safety_threshold(result: ModerationResult, thresholds: dict) -> bool:
    """Applies category thresholds to decide whether to allow text."""
    for category, severity in result.categories.items():
        if category in thresholds and severity > thresholds[category]:
            return False  # Not allowed if any category exceeds its threshold
    return True  # Allowed if all categories are below or at their thresholds
