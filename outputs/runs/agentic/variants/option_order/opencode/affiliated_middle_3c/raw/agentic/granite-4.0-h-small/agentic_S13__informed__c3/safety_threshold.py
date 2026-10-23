def apply_category_threshold(severity: str, threshold: float) -> bool:
    """Applies a category-specific threshold to decide whether to allow text.

    Args:
        severity (str): Severity level (LOW/MEDIUM/HIGH) from moderation.
        threshold (float): Threshold (0.0 - 1.0) for the category.

    Returns:
        bool: True if text passes (severity LOW or MEDIUM with score <= threshold), False otherwise.
    """
    severity_order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
    return severity_order[severity] <= 1 and severity_order[severity] <= threshold
