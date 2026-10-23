from __future__ import annotations

from typing import Dict, Iterable, Optional

from safety_client import PerspectiveSafetyClient
from safety_models import SafetyDecision, clamp_score, normalize_perspective_scores


DEFAULT_THRESHOLDS: Dict[str, float] = {
    "toxicity": 0.82,
    "severe_toxicity": 0.55,
    "threat": 0.4,
    "identity_attack": 0.65,
    "profanity": 0.9,
    "insult": 0.78,
    "sexually_explicit": 0.75,
}


def apply_safety_threshold(
    text: str,
    *,
    category_thresholds: Optional[Dict[str, float]] = None,
    attributes: Optional[Iterable[str]] = None,
    language: str = "en",
) -> SafetyDecision:
    client = PerspectiveSafetyClient()
    response = client.analyze_text(text=text, attributes=attributes, language=language)
    categories = normalize_perspective_scores(response.get("attributeScores", {}))
    thresholds = {**DEFAULT_THRESHOLDS, **(category_thresholds or {})}
    triggered = {
        name: score
        for name, score in categories.items()
        if score >= clamp_score(thresholds.get(name, 1.0))
    }
    reason = max(triggered, key=triggered.get) if triggered else None
    return SafetyDecision(
        text=text,
        flagged=bool(triggered),
        categories=categories,
        block_reason=reason,
        raw_response={"thresholds": thresholds, "provider_response": response},
    )
