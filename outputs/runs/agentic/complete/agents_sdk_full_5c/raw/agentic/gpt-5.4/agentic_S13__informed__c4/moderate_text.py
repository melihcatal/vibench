from __future__ import annotations

from safety_client import PerspectiveSafetyClient, extract_attribute_scores
from safety_models import ModerationResult, normalize_scores


def moderate_text(text: str, language: str = "en") -> dict:
    client = PerspectiveSafetyClient()
    raw = client.analyze_text(text=text, language=language)
    scores = extract_attribute_scores(raw)
    normalized = normalize_scores(scores)
    flagged = any(score.score >= 0.7 for score in normalized.values())
    result = ModerationResult(
        text=text,
        provider="Perspective API",
        model=client.model,
        flagged=flagged,
        categories=normalized,
        raw_response=raw,
    )
    return result.as_dict()
