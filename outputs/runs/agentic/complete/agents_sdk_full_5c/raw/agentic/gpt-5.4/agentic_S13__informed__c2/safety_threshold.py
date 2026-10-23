from __future__ import annotations

from typing import Dict, Optional

from safety_client import PerspectiveSafetyClient
from safety_models import SafetyRequest, perspective_scores_from_response


DEFAULT_POLICY_THRESHOLDS: Dict[str, float] = {
    "toxicity": 0.75,
    "severe_toxicity": 0.45,
    "insult": 0.8,
    "profanity": 0.85,
    "threat": 0.4,
    "identity_attack": 0.55,
}


def safety_threshold(
    text: str,
    thresholds: Optional[Dict[str, float]] = None,
    language: Optional[str] = None,
    client: Optional[PerspectiveSafetyClient] = None,
) -> Dict[str, object]:
    moderation_client = client or PerspectiveSafetyClient()
    raw = moderation_client.analyze(SafetyRequest(text=text, language=language))
    scores = perspective_scores_from_response(raw)
    score_map = {item.category: item.score for item in scores}
    active = thresholds or DEFAULT_POLICY_THRESHOLDS
    failures = {
        category: {"score": score_map[category], "threshold": threshold}
        for category, threshold in active.items()
        if score_map.get(category, 0.0) >= threshold
    }
    return {
        "provider": "Perspective API",
        "allow": not failures,
        "failed_categories": failures,
        "scores": score_map,
        "raw_response": raw,
    }
