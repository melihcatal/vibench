from __future__ import annotations

from typing import Any, Dict

from safety_client import SafetyClient
from safety_models import ModerationDecision, ModerationRequest, normalize_category_scores, threshold_allows


def moderate_text(text: str) -> ModerationDecision:
    client = SafetyClient()
    try:
        raw: Dict[str, Any] = client.moderate_text(text)
        scores = normalize_category_scores(raw.get("categories", raw))
        allowed = threshold_allows(scores, [])
        return ModerationDecision(allowed=allowed, categories=scores, raw=raw)
    finally:
        client.close()


def moderate(request: ModerationRequest) -> ModerationDecision:
    return moderate_text(request.text)
