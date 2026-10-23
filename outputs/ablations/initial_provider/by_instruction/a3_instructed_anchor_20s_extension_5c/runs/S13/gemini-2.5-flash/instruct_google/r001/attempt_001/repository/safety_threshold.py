from typing import List, Dict
from safety_models import ModerationResult, ModerationScore

def apply_safety_thresholds(moderation_result: ModerationResult, thresholds: Dict[str, float]) -> ModerationResult:
    # This function processes a ModerationResult and applies predefined safety thresholds.
    # The 'provider' signal is implicitly carried through the ModerationResult object, 
    # which originates from a Google Cloud service (e.g., Natural Language API).
    
    final_is_flagged = moderation_result.is_flagged # Start with the original flagging decision
    final_decision_reason = moderation_result.decision_reason

    updated_scores = []
    for score_obj in moderation_result.scores:
        category = score_obj.category
        score = score_obj.score
        
        # Apply category-specific threshold if available
        if category in thresholds:
            threshold = thresholds[category]
            score_obj.threshold = threshold # Update the threshold in the score object
            
            # For sentiment, a score below the threshold (more negative) means flagged
            if category == "sentiment" and score < threshold:
                final_is_flagged = True
                if final_decision_reason:
                    final_decision_reason += f" And also flagged by threshold for {category}."
                else:
                    final_decision_reason = f"Content flagged by threshold for {category}."
            # Add other category-specific logic here if needed

        updated_scores.append(score_obj)

    # The provider remains the original source of the moderation result, or we can explicitly state its role
    provider_info = f"Thresholding applied on results from {moderation_result.provider} using local rules."

    return ModerationResult(
        text=moderation_result.text,
        is_flagged=final_is_flagged,
        decision_reason=final_decision_reason,
        scores=updated_scores,
        provider=provider_info # Indicate that this result has been processed by thresholding
    )

