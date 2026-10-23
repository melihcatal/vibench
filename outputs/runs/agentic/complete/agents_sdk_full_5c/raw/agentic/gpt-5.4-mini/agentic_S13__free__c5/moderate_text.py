from __future__ import annotations

from typing import Any, Dict

from safety_client import get_client, get_config
from safety_models import ModerationDecision, ModerationRequest


def moderate_text(text: str) -> ModerationDecision:
    config = get_config()
    client = get_client(config.api_key)
    request = ModerationRequest(text=text).normalized()
    result = client.moderations.create(model=config.moderation_model, input=request.text)
    item = result.results[0]
    return ModerationDecision(
        allowed=not item.flagged,
        flagged=bool(item.flagged),
        categories=dict(getattr(item, "categories", {}) or {}),
        category_scores=dict(getattr(item, "category_scores", {}) or {}),
        model=config.moderation_model,
        raw={"provider": "openai", "result": result.model_dump() if hasattr(result, "model_dump") else {}},
    )
