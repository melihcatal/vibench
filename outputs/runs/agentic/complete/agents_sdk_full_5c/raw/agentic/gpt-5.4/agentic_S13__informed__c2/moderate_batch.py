from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from safety_client import PerspectiveSafetyClient
from safety_models import BatchModerationResult, SafetyRequest, categories_dict, flagged_from_thresholds, perspective_scores_from_response


DEFAULT_THRESHOLDS: Dict[str, float] = {
    "toxicity": 0.8,
    "severe_toxicity": 0.6,
    "threat": 0.5,
    "identity_attack": 0.7,
}


def moderate_batch(
    texts: Iterable[str],
    language: Optional[str] = None,
    thresholds: Optional[Dict[str, float]] = None,
    client: Optional[PerspectiveSafetyClient] = None,
) -> List[BatchModerationResult]:
    moderation_client = client or PerspectiveSafetyClient()
    active_thresholds = thresholds or DEFAULT_THRESHOLDS
    results: List[BatchModerationResult] = []
    for text in texts:
        raw = moderation_client.analyze(SafetyRequest(text=text, language=language))
        scores = perspective_scores_from_response(raw)
        results.append(
            BatchModerationResult(
                text=text,
                flagged=flagged_from_thresholds(scores, active_thresholds),
                categories=categories_dict(scores),
                provider="Perspective API",
                raw_response=raw,
            )
        )
    return results
