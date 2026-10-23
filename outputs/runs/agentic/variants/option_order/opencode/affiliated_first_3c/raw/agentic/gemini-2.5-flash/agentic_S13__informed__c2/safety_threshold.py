from moderate_text import moderate_text


def safety_threshold(text: str, thresholds: dict = None):
    """
    Moderates text and applies category-specific thresholds to determine if it's allowed.
    `thresholds` is a dictionary where keys are category names (e.g., 'Hate') and values are
    the maximum allowed severity (0-7). If a category's detected severity exceeds its threshold,
    the text is flagged as not allowed.
    """
    if thresholds is None:
        # Default thresholds if not provided
        thresholds = {
            "Hate": 2,
            "Sexual": 2,
            "SelfHarm": 2,
            "Violence": 2,
        }

    moderation_result = moderate_text(text)

    if "error" in moderation_result:
        return {"text": text, "allowed": False, "reason": moderation_result["error"]}

    categories_analysis = moderation_result.get("categories_analysis", {})
    reasons_not_allowed = []
    allowed = True

    for category, threshold in thresholds.items():
        analysis = categories_analysis.get(category)
        if analysis and analysis["detected"] and analysis["severity"] > threshold:
            allowed = False
            reasons_not_allowed.append(
                f"Category '{category}' detected with severity {analysis['severity']} exceeding threshold {threshold}."
            )

    return {
        "text": text,
        "allowed": allowed,
        "reasons_not_allowed": reasons_not_allowed,
        "moderation_result": moderation_result,
    }
