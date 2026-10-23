from __future__ import annotations

from typing import Dict

from safety_client import get_client, get_config


DEFAULT_THRESHOLDS: Dict[str, float] = {
    "hate": 0.4,
    "hate/threatening": 0.2,
    "harassment": 0.5,
    "self-harm": 0.2,
    "sexual": 0.5,
    "violence": 0.5,
}


def allow_text(text: str, thresholds: Dict[str, float] | None = None) -> bool:
    config = get_config()
    client = get_client(config.api_key)
    thresholds = thresholds or DEFAULT_THRESHOLDS
    result = client.moderations.create(model=config.moderation_model, input=text)
    item = result.results[0]
    scores = dict(getattr(item, "category_scores", {}) or {})
    for category, threshold in thresholds.items():
        if scores.get(category, 0.0) >= threshold:
            return False
    return not bool(item.flagged)
