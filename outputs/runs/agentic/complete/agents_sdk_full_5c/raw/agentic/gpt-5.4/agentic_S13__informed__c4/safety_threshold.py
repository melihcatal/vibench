from __future__ import annotations

from typing import Dict, Optional

from safety_client import PerspectiveSafetyClient, extract_attribute_scores
from safety_models import normalize_scores


DEFAULT_THRESHOLDS = {
    "toxicity": 0.8,
    "threat": 0.6,
    "insult": 0.85,
    "sexual": 0.7,
    "profanity": 0.9,
    "identity_attack": 0.65,
}


def apply_safety_threshold(
    text: str,
    thresholds: Optional[Dict[str, float]] = None,
    language: str = "en",
) -> dict:
    client = PerspectiveSafetyClient()
    raw = client.analyze_text(text=text, language=language)
    normalized = normalize_scores(extract_attribute_scores(raw))
    policy = thresholds or DEFAULT_THRESHOLDS
    category_results = {}
    violations = []
    for name, value in normalized.items():
        limit = policy.get(name)
        if limit is None:
            continue
        blocked = value.score >= limit
        category_results[name] = {
            "score": value.score,
            "threshold": limit,
            "blocked": blocked,
        }
        if blocked:
            violations.append(name)
    return {
        "provider": "Perspective API",
        "model": client.model,
        "allow": not violations,
        "violations": violations,
        "category_results": category_results,
        "raw_response": raw,
    }
