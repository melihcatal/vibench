from typing import List
from safety_models import ModerationResult, SafetyRating, ThresholdConfig

def apply_safety_threshold(moderation_result: ModerationResult, thresholds: List[ThresholdConfig]) -> ModerationResult:
    """
    Applies category thresholds to decide whether to allow text.
    Modifies the ModerationResult.is_allowed and ModerationResult.reasons based on thresholds.
    """
    updated_result = moderation_result
    updated_result.is_allowed = True
    updated_result.reasons = []

    # Define a mapping from string probability names to a comparable order
    probability_order = {
        "HARM_BLOCK_THRESHOLD_UNSPECIFIED": 0,
        "BLOCK_LOW_AND_ABOVE": 1,
        "BLOCK_MEDIUM_AND_ABOVE": 2,
        "BLOCK_HIGH_AND_ABOVE": 3,
        "BLOCK_ONLY_HIGH": 4,
        "DO_NOT_BLOCK": 5
    }

    # Mapping for Vertex AI's specific probability outputs to a comparable order for blocking logic
    vertex_probability_order = {
        "NEGLIGIBLE": 0,
        "VERY_UNLIKELY": 1,
        "UNLIKELY": 2,
        "POSSIBLE": 3,
        "LIKELY": 4,
        "VERY_LIKELY": 5
    }

    # Iterate through each safety rating in the moderation result
    for rating in updated_result.safety_ratings:
        for threshold in thresholds:
            if rating.category == threshold.category:
                # Determine if the content should be blocked based on the threshold
                # This logic assumes higher vertex_probability_order means more severe
                # And higher probability_order means a stricter block threshold
                if (rating.blocked or  # If the model already blocked it
                    (vertex_probability_order.get(rating.probability, 0) > 0 and
                     probability_order.get(threshold.block_probability, 0) <= vertex_probability_order.get(rating.probability, 0))):

                    updated_result.is_allowed = False
                    updated_result.reasons.append(
                        f"Blocked by threshold for {rating.category} with probability {rating.probability} "
                        f"against threshold {threshold.block_probability}"
                    )
                    break # No need to check other thresholds for this category if already blocked
    return updated_result
