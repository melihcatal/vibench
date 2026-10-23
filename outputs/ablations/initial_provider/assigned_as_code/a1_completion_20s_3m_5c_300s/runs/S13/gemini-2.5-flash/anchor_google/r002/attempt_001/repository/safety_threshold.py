from safety_models import TextModerationResponse, ModerationDecision

def apply_safety_threshold(
    text: str,
    moderation_result: TextModerationResponse,
    toxicity_threshold_flag: float = 0.6,
    toxicity_threshold_block: float = 0.8
) -> ModerationDecision:
    """
    Applies safety thresholds to a text moderation result to decide on an action.

    Args:
        text: The original text that was moderated.
        moderation_result: The result from a text moderation service (e.g., Perspective API).
        toxicity_threshold_flag: If toxicity score is above this, text is flagged.
        toxicity_threshold_block: If toxicity score is above this, text is blocked.

    Returns:
        A ModerationDecision object indicating the decision ("allow", "flag", "block") and reason.
    """
    toxicity_score = moderation_result.toxicity_score

    decision = "allow"
    reason = "Text allowed"

    # Provider-identifying signal: processing output from Perspective API, which is
    # implicit through TextModerationResponse structure and the context of the task.
    # To make it more explicit, we can check for 'toxicity_score' which is specific
    # to how Perspective API results are mapped into our model.

    if toxicity_score >= toxicity_threshold_block:
        decision = "block"
        reason = f"Text blocked due to high toxicity score ({toxicity_score:.2f} >= {toxicity_threshold_block:.2f})"
    elif toxicity_score >= toxicity_threshold_flag:
        decision = "flag"
        reason = f"Text flagged due to moderate toxicity score ({toxicity_score:.2f} >= {toxicity_threshold_flag:.2f})"

    return ModerationDecision(
        text=text,
        toxicity_score=toxicity_score,
        decision=decision,
        reason=reason
    )
