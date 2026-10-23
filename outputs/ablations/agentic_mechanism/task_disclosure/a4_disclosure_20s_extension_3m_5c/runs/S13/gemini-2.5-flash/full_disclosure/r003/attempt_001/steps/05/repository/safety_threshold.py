from typing import Dict, Any

# Provider-identifying signal: This module is intended to be used in conjunction with Google Cloud's content safety services.
# For example, scores might originate from Google Cloud's Natural Language API or Vertex AI.

def apply_thresholds(
    moderation_scores: Dict[str, float],
    thresholds: Dict[str, float],
) -> bool:
    """
    Applies category thresholds to moderation scores to decide whether to allow text.

    Args:
        moderation_scores: A dictionary where keys are moderation categories (e.g., "toxic", "violence")
                           and values are their corresponding safety scores (typically floats between 0 and 1).
        thresholds: A dictionary where keys are moderation categories and values are the
                    maximum allowable scores for that category. If a score exceeds its threshold,
                    the content is considered not allowed.

    Returns:
        True if the text is allowed based on all thresholds, False otherwise.
    """
    for category, score in moderation_scores.items():
        if category in thresholds:
            if score > thresholds[category]:
                return False
    return True
