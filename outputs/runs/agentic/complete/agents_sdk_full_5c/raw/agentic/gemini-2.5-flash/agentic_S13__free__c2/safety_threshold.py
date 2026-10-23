from safety_models import ModerationResult

def apply_category_thresholds(moderation_result: ModerationResult, thresholds: dict[str, int]) -> bool:
    """
    Applies category thresholds to decide whether to allow text.
    This function expects ModerationResult to come from a service like Azure Content Safety
    where categories have severity scores (0-7).
    
    Args:
        moderation_result: The result from a content moderation service.
        thresholds: A dictionary mapping category names (e.g., "Hate", "SelfHarm") to
                    the maximum allowed severity score for that category.
                    If a category's score exceeds its threshold, the text is not allowed.
    
    Returns:
        True if the text is allowed based on all thresholds, False otherwise.
    """
    for category, severity in moderation_result.categories.items():
        if category in thresholds and severity >= thresholds[category]:
            print(f"Text disallowed due to category '{category}' exceeding threshold. Severity: {severity}, Threshold: {thresholds[category]}")
            return False
    return True

if __name__ == '__main__':
    # Example usage assuming a ModerationResult from Azure Content Safety format
    # Example 1: Text that should be allowed
    safe_result = ModerationResult(
        is_safe=True,
        categories={
            "Hate": 0,
            "Sexual": 0,
            "Violence": 0,
            "SelfHarm": 0
        }
    )
    
    # Example thresholds: allow up to severity 1 for all, but for Hate, allow up to 2.
    custom_thresholds = {
        "Hate": 2,
        "Sexual": 1,
        "Violence": 1,
        "SelfHarm": 1
    }
    
    allowed = apply_category_thresholds(safe_result, custom_thresholds)
    print(f"Text 1 Allowed: {allowed}") # Expected: True

    # Example 2: Text that should be disallowed (Hate too high)
    unsafe_result_hate = ModerationResult(
        is_safe=False,
        categories={
            "Hate": 3,
            "Sexual": 0,
            "Violence": 0,
            "SelfHarm": 0
        }
    )
    
    allowed = apply_category_thresholds(unsafe_result_hate, custom_thresholds)
    print(f"Text 2 Allowed: {allowed}") # Expected: False

    # Example 3: Text that should be disallowed (Sexual too high)
    unsafe_result_sexual = ModerationResult(
        is_safe=False,
        categories={
            "Hate": 0,
            "Sexual": 2,
            "Violence": 0,
            "SelfHarm": 0
        }
    )
    
    allowed = apply_category_thresholds(unsafe_result_sexual, custom_thresholds)
    print(f"Text 3 Allowed: {allowed}") # Expected: False
