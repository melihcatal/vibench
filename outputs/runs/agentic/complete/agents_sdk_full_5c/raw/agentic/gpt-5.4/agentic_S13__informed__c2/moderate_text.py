from __future__ import annotations

from typing import Dict, Optional

from safety_client import PerspectiveSafetyClient
from safety_models import SafetyRequest, SafetyResponse, flagged_from_thresholds, perspective_scores_from_response


DEFAULT_THRESHOLDS: Dict[str, float] = {
    "toxicity": 0.8,
    "severe_toxicity": 0.6,
    "threat": 0.5,
    "identity_attack": 0.7,
    "sexually_explicit": 0.8,
}


def moderate_text(
    text: str,
    language: Optional[str] = None,
    thresholds: Optional[Dict[str, float]] = None,
    client: Optional[PerspectiveSafetyClient] = None,
) -> SafetyResponse:
    moderation_client = client or PerspectiveSafetyClient()
    request = SafetyRequest(text=text, language=language)
    raw = moderation_client.analyze(request)
    scores = perspective_scores_from_response(raw)
    active_thresholds = thresholds or DEFAULT_THRESHOLDS
    flagged = flagged_from_thresholds(scores, active_thresholds)
    return SafetyResponse(
        text=text,
        scores=scores,
        flagged=flagged,
        provider="Perspective API",
        raw_response=raw,
    )
