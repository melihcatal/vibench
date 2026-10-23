def apply_safety_thresholds(moderation_result: dict, thresholds: dict) -> dict:
    """
    Applies category thresholds to decide whether to allow text.
    
    Args:
        moderation_result (dict): The result from a moderation service, e.g., from moderate_text.py.
                                  Expected format: {"category_name": {"severity": int}}
        thresholds (dict): A dictionary of thresholds for each category.
                           Expected format: {"category_name": {"max_severity": int}}
                           
    Returns:
        dict: A dictionary indicating whether the text is allowed and reasons if not.
              Format: {"is_allowed": bool, "reasons": list[str]}
    """
    is_allowed = True
    reasons = []

    for category, result in moderation_result.items():
        if category in thresholds:
            max_severity = thresholds[category]["max_severity"]
            if result["severity"] >= max_severity:
                is_allowed = False
                reasons.append(f"Category '{category}' exceeded max severity threshold (severity: {result["severity"]}, threshold: {max_severity}).")
    
    return {"is_allowed": is_allowed, "reasons": reasons}
