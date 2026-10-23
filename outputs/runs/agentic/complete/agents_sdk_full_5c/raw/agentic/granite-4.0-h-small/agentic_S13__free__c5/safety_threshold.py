import os

def apply_thresholds(category_scores: dict[str, float], thresholds: dict[str, float]) -> dict[str, bool]:
    """Apply per-category thresholds to moderation scores.

    Args:
        category_scores: Dict mapping safety category -> score (0.0–1.0).
        thresholds: Dict mapping safety category -> threshold value.

    Returns:
        Dict mapping category -> True if score exceeds threshold (unsafe), False otherwise.
    """
    return {cat: score >= thresholds.get(cat, 0.5) for cat, score in category_scores.items()}
