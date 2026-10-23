from safety_models import ThresholdRequest, ThresholdDecision


def apply_safety_threshold(request: ThresholdRequest) -> ThresholdDecision:
    """
    Applies custom thresholds to moderation scores to make a decision.
    This is a local business logic helper and does not call an external API.
    """
    is_allowed = True
    violated_categories = []

    for score in request.scores:
        threshold = request.thresholds.get(score.category)
        if threshold is not None and score.severity >= threshold:
            is_allowed = False
            violated_categories.append(score.category)

    return ThresholdDecision(allow=is_allowed, violated_categories=violated_categories)
