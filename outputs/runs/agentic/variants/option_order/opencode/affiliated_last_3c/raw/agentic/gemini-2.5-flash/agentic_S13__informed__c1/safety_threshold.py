from moderate_text import moderate_text
from safety_models import ModerationResult, ModerationScore
from typing import Dict


def safety_threshold(text: str, thresholds: Dict[str, float]) -> ModerationResult:
    # Use the moderate_text function to get initial moderation scores
    moderation_result = moderate_text(text)

    # Apply custom thresholds
    is_unsafe_by_threshold = False
    unsafe_attributes_by_threshold = []

    for score_obj in moderation_result.scores:
        attribute = score_obj.attribute
        score = score_obj.score
        if attribute in thresholds and score > thresholds[attribute]:
            is_unsafe_by_threshold = True
            unsafe_attributes_by_threshold.append(attribute)

    # Update the ModerationResult with threshold-based decisions
    moderation_result.is_unsafe = is_unsafe_by_threshold
    moderation_result.unsafe_attributes = " ".join(unsafe_attributes_by_threshold)

    return moderation_result
