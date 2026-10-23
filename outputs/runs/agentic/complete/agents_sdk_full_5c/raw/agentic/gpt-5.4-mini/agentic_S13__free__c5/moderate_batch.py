from __future__ import annotations

from typing import List

from safety_client import get_client, get_config
from safety_models import BatchModerationItem, BatchModerationResponse, ModerationDecision, normalize_text


def moderate_batch(messages: List[str]) -> BatchModerationResponse:
    config = get_config()
    client = get_client(config.api_key)
    normalized = [normalize_text(m) for m in messages]
    result = client.moderations.create(model=config.moderation_model, input=normalized)
    items = []
    for idx, (text, decision) in enumerate(zip(normalized, result.results)):
        items.append(
            BatchModerationItem(
                index=idx,
                text=text,
                decision=ModerationDecision(
                    allowed=not decision.flagged,
                    flagged=bool(decision.flagged),
                    categories=dict(getattr(decision, "categories", {}) or {}),
                    category_scores=dict(getattr(decision, "category_scores", {}) or {}),
                    model=config.moderation_model,
                    raw={"provider": "openai"},
                ),
            )
        )
    return BatchModerationResponse(items=items)
