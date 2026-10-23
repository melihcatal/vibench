from safety_client import call_moderation, OPENAI_MODERATION_MODEL
from safety_models import (
    ModerationResult,
    ThresholdConfig,
    ThresholdDecision,
    normalize_moderation_response,
    normalize_category_name,
    truncate_text,
)


def _build_threshold_map(config):
    return {
        "hate": config.hate,
        "hate_threatening": config.hate_threatening,
        "self_harm": config.self_harm,
        "sexual": config.sexual,
        "sexual_minors": config.sexual_minors,
        "violence": config.violence,
        "violence_graphic": config.violence_graphic,
        "harassment": config.harassment,
        "harassment_threatening": config.harassment_threatening,
        "illicit": config.illicit,
        "illicit_violent": config.illicit_violent,
        "self_harm_intent": config.self_harm_intent,
        "self_harm_instructions": config.self_harm_instructions,
        "sexualizing_minors": config.sexualizing_minors,
    }


def apply_safety_threshold(text, config=None, model=None):
    if config is None:
        config = ThresholdConfig()
    threshold_map = _build_threshold_map(config)
    truncated = truncate_text(text)
    raw_response = call_moderation(truncated, model=model or OPENAI_MODERATION_MODEL)
    result = normalize_moderation_response(raw_response)

    exceeded_categories = []
    scores = {}
    for cs in result.category_scores:
        scores[cs.name] = cs.score
        threshold = threshold_map.get(cs.name, 0.5)
        if cs.score >= threshold:
            exceeded_categories.append(cs.name)

    allowed = len(exceeded_categories) == 0
    return ThresholdDecision(
        allowed=allowed,
        exceeded_categories=exceeded_categories,
        scores=scores,
    )


def apply_safety_threshold_with_summary(text, config=None, model=None):
    decision = apply_safety_threshold(
        text, config=config, model=model or OPENAI_MODERATION_MODEL
    )
    summary = {
        "allowed": decision.allowed,
        "exceeded_categories": decision.exceeded_categories,
        "scores": decision.scores,
        "thresholds_applied": {
            "hate": config.hate if config else ThresholdConfig().hate,
            "sexual": config.sexual if config else ThresholdConfig().sexual,
            "violence": config.violence if config else ThresholdConfig().violence,
            "harassment": config.harassment if config else ThresholdConfig().harassment,
            "self_harm": config.self_harm if config else ThresholdConfig().self_harm,
        },
    }
    return summary
