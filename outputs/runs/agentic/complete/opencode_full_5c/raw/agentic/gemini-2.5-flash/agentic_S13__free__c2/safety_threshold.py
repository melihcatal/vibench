from safety_models import ModerationDecision, ModerationCategory, ModerationResult


def apply_safety_thresholds(
    moderation_result: ModerationResult, thresholds: dict
) -> ModerationDecision:
    """Applies category thresholds to decide whether to allow text."""
    for category, score in moderation_result.scores.items():
        if category in thresholds and score >= thresholds[category]:
            return ModerationDecision(
                allow=False,
                reason=f"Content exceeded threshold for category: {category}",
            )
    return ModerationDecision(
        allow=True, reason="Content within acceptable thresholds."
    )
