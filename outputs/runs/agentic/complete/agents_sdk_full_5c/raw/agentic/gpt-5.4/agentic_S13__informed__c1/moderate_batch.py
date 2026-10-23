from __future__ import annotations

from typing import Iterable, List, Optional

from safety_client import PerspectiveSafetyClient
from safety_models import BatchSafetyDecision, SafetyDecision, normalize_perspective_scores, top_category


DEFAULT_BLOCK_THRESHOLD = 0.8


def moderate_batch(
    messages: Iterable[str],
    *,
    attributes: Optional[Iterable[str]] = None,
    language: str = "en",
    block_threshold: float = DEFAULT_BLOCK_THRESHOLD,
) -> BatchSafetyDecision:
    client = PerspectiveSafetyClient()
    decisions: List[SafetyDecision] = []
    for text in messages:
        response = client.analyze_text(text=text, attributes=attributes, language=language)
        categories = normalize_perspective_scores(response.get("attributeScores", {}))
        flagged = any(score >= block_threshold for score in categories.values())
        decisions.append(
            SafetyDecision(
                text=text,
                flagged=flagged,
                categories=categories,
                block_reason=top_category(categories) if flagged else None,
                raw_response=response,
            )
        )
    return BatchSafetyDecision(decisions=decisions)
