from safety_models import ModerationResult, Thresholds


def is_text_allowed(
    moderation_result: ModerationResult, thresholds: Thresholds
) -> bool:
    """
    Applies category thresholds from an OpenAI moderation result to decide whether to allow text.
    """
    scores = moderation_result.category_scores

    if scores.hate > thresholds.hate:
        return False
    if scores.sexual > thresholds.sexual:
        return False
    if scores.violence > thresholds.violence:
        return False
    if scores.harassment > thresholds.harassment:
        return False
    if scores.self_harm > thresholds.self_harm:
        return False

    # The OpenAI model also provides boolean flags
    if moderation_result.flagged:
        return False

    return True
