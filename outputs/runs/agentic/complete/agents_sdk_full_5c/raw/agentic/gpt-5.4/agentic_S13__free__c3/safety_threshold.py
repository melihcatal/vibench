from __future__ import annotations

from typing import Dict

from safety_client import DEFAULT_MODERATION_MODEL, get_openai_client
from safety_models import category_score_map, normalize_openai_result


DEFAULT_THRESHOLDS: Dict[str, float] = {
    "violence": 0.6,
    "self-harm": 0.4,
    "sexual/minors": 0.01,
    "hate": 0.5,
    "harassment": 0.7,
}


def apply_safety_threshold(text: str, thresholds: Dict[str, float] | None = None) -> dict:
    client = get_openai_client()
    response = client.moderations.create(model=DEFAULT_MODERATION_MODEL, input=text)
    decision = normalize_openai_result(response.results[0], model=DEFAULT_MODERATION_MODEL)
    score_map = category_score_map(decision)
    active_thresholds = thresholds or DEFAULT_THRESHOLDS

    exceeded = {
        category: score_map.get(category, 0.0)
        for category, threshold in active_thresholds.items()
        if score_map.get(category, 0.0) >= threshold
    }

    return {
        "provider": "OpenAI",
        "model": DEFAULT_MODERATION_MODEL,
        "allow": not exceeded,
        "flagged": decision.flagged,
        "exceeded": exceeded,
        "scores": score_map,
    }
