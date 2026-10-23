from __future__ import annotations

from typing import Iterable, Optional

from safety_client import PerspectiveSafetyClient
from safety_models import SafetyDecision, normalize_perspective_scores, top_category


DEFAULT_BLOCK_THRESHOLD = 0.8


def moderate_text(
    text: str,
    *,
    attributes: Optional[Iterable[str]] = None,
    language: str = "en",
    block_threshold: float = DEFAULT_BLOCK_THRESHOLD,
) -> SafetyDecision:
    client = PerspectiveSafetyClient()
    response = client.analyze_text(text=text, attributes=attributes, language=language)
    categories = normalize_perspective_scores(response.get("attributeScores", {}))
    flagged = any(score >= block_threshold for score in categories.values())
    reason = top_category(categories) if flagged else None
    return SafetyDecision(
        text=text,
        flagged=flagged,
        categories=categories,
        block_reason=reason,
        raw_response=response,
    )
