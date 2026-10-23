from typing import Dict, Any

def safety_threshold(moderation_scores: Dict[str, float], thresholds: Dict[str, float]) -> Dict[str, Any]:
    """
    Applies category thresholds to decide whether to allow text.

    Args:
        moderation_scores: A dictionary of moderation scores (e.g., {"toxicity": 0.8})
        thresholds: A dictionary of thresholds for each category (e.g., {"toxicity": 0.7})

    Returns:
        A dictionary indicating whether the text is allowed and reasons for blocking.
    """
    is_allowed = True
    reasons = []

    for category, score in moderation_scores.items():
        if category in thresholds:
            if score > thresholds[category]:
                is_allowed = False
                reasons.append(f"'{category}' score ({score:.2f}) exceeds threshold ({thresholds[category]:.2f})")
    
    return {
        "is_allowed": is_allowed,
        "reasons": reasons
    }
