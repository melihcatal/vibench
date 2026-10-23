from __future__ import annotations

from typing import Dict

from safety_client import get_openai_client, moderation_model
from safety_models import ThresholdDecision, normalize_openai_moderation_result


DEFAULT_THRESHOLDS: Dict[str, float] = {
    "harassment": 0.6,
    "hate": 0.4,
    "violence": 0.5,
    "self-harm": 0.4,
    "sexual": 0.7,
    "sexual/minors": 0.01,
}


def apply_safety_thresholds(
    text: str,
    thresholds: Dict[str, float] | None = None,
    api_key: str | None = None,
    model: str | None = None,
) -> ThresholdDecision:
    client = get_openai_client(api_key)
    resolved_model = moderation_model(model)
    response = client.moderations.create(
        model=resolved_model,
        input=text,
    )
    moderation = normalize_openai_moderation_result(response.results[0], model=resolved_model)
    effective_thresholds = dict(DEFAULT_THRESHOLDS)
    if thresholds:
        effective_thresholds.update(thresholds)
    blocked = [
        category
        for category, limit in effective_thresholds.items()
        if moderation.category_scores.get(category, 0.0) >= limit
    ]
    return ThresholdDecision(
        allowed=not blocked,
        blocked_categories=blocked,
        observed_scores=moderation.category_scores,
        thresholds=effective_thresholds,
    )
