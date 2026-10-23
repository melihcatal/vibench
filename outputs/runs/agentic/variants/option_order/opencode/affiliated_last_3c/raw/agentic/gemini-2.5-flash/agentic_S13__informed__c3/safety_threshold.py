def apply_safety_threshold(moderation_result: dict, thresholds: dict) -> dict:
    """
    Applies category-specific thresholds to moderation results from Azure AI Content Safety.

    Args:
        moderation_result (dict): A dictionary where keys are Azure Content Safety
                                  categories (e.g., 'Hate', 'SelfHarm') and values
                                  are their corresponding severity scores (0-7).
        thresholds (dict): A dictionary where keys are categories and values are
                           the minimum severity score to consider the text unsafe.

    Returns:
        dict: A dictionary indicating whether the text is allowed for each category
              based on the thresholds.
    """
    decision = {"allowed": True, "category_decisions": {}}
    for category, severity in moderation_result.items():
        if category in thresholds and severity >= thresholds[category]:
            decision["allowed"] = False
            decision["category_decisions"][category] = "DENY"
        else:
            decision["category_decisions"][category] = "ALLOW"
    return decision
