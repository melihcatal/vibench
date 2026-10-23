from typing import Dict, Literal
from safety_models import ModerationResponse, SafetyRating, SafetyAttribute

Threshold = Literal["BLOCK_NONE", "BLOCK_LOW_AND_ABOVE", "BLOCK_MEDIUM_AND_ABOVE", "BLOCK_HIGH_AND_ABOVE"]

def apply_safety_thresholds(
    moderation_response: ModerationResponse,
    thresholds: Dict[str, Threshold]
) -> bool:
    """
    Applies category thresholds to decide whether to allow text.
    Returns True if allowed, False if blocked.
    """
    probability_map = {
        "NEGLIGIBLE": 0,
        "UNLIKELY": 1,
        "POSSIBLE": 2,
        "LIKELY": 3,
        "VERY_LIKELY": 4
    }

    threshold_map = {
        "BLOCK_NONE": 5, # Effectively never block based on this threshold
        "BLOCK_LOW_AND_ABOVE": 1,
        "BLOCK_MEDIUM_AND_ABOVE": 2,
        "BLOCK_HIGH_AND_ABOVE": 3
    }

    if not moderation_response.results:
        return True # Allow if no safety attributes are found

    for result in moderation_response.results:
        for rating in result.categories:
            category = rating.category
            if category in thresholds:
                required_threshold_level = threshold_map[thresholds[category]]
                actual_probability_level = probability_map.get(rating.probability, 0)

                if actual_probability_level >= required_threshold_level:
                    return False  # Blocked due to threshold

    return True  # Allowed if no thresholds are met for blocking
