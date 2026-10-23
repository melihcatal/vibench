from typing import Dict

def apply_category_thresholds(results: Dict[str, float], thresholds: Dict[str, float]) -> bool:
    """Apply per‑category thresholds to decide whether text passes moderation.

    * results: dictionary returned by the moderation service where keys are category
      names (e.g., \"hate\", \"self_harm\", \"sexual\") and values are scores 0‑1.
    * thresholds: mapping of category to the minimum acceptable score. If a category
      score exceeds its threshold the text is considered unsafe.
    
    Returns True if the text is safe (all scores below their respective thresholds).
    """
    for category, score in results.items():
        if category in thresholds and score >= thresholds[category]:
            return False  # unsafe
    return True  # safe

# Example default thresholds (could be loaded from config or environment)
def default_thresholds() -> Dict[str, float]:
    return {
        "hate": 0.7,
        "self_harm": 0.6,
        "sexual": 0.8,
        "violence": 0.7,
    }
