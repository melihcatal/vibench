import os
from typing import Any, Dict, Mapping, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


DEFAULT_THRESHOLDS: Dict[str, float] = {
    "harassment": 0.5,
    "hate": 0.5,
    "self-harm": 0.5,
    "sexual": 0.5,
    "violence": 0.5,
}


class SafetyThresholdError(RuntimeError):
    pass


def _normalize_scores(result: Mapping[str, Any]) -> Dict[str, float]:
    scores: Dict[str, float] = {}
    categories = result.get("category_scores") or {}
    if isinstance(categories, Mapping):
        for key, value in categories.items():
            try:
                scores[str(key)] = float(value)
            except (TypeError, ValueError):
                continue
    return scores


def _map_provider_categories(scores: Mapping[str, float]) -> Dict[str, float]:
    mapped: Dict[str, float] = {}
    for key, value in scores.items():
        normalized = key.lower().replace("_", "-")
        if "harass" in normalized:
            mapped["harassment"] = max(mapped.get("harassment", 0.0), value)
        elif "hate" in normalized:
            mapped["hate"] = max(mapped.get("hate", 0.0), value)
        elif "self-harm" in normalized or "selfharm" in normalized:
            mapped["self-harm"] = max(mapped.get("self-harm", 0.0), value)
        elif "sexual" in normalized:
            mapped["sexual"] = max(mapped.get("sexual", 0.0), value)
        elif "violence" in normalized or "violent" in normalized:
            mapped["violence"] = max(mapped.get("violence", 0.0), value)
    return mapped


def evaluate_text(text: str, thresholds: Optional[Mapping[str, float]] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
    if not text:
        return {"allow": True, "reason": "empty_text", "scores": {}, "thresholds": dict(thresholds or DEFAULT_THRESHOLDS)}

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise SafetyThresholdError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODEL, "input": text},
        timeout=30,
    )
    if response.status_code >= 400:
        raise SafetyThresholdError(f"OpenAI moderation request failed: {response.status_code} {response.text}")

    payload = response.json()
    results = payload.get("results") or []
    if not results:
        raise SafetyThresholdError("OpenAI moderation response missing results")

    item = results[0] if isinstance(results, list) else {}
    scores = _map_provider_categories(_normalize_scores(item))
    active_thresholds = dict(DEFAULT_THRESHOLDS)
    if thresholds:
        active_thresholds.update({str(k): float(v) for k, v in thresholds.items()})

    violations = {
        category: score
        for category, score in scores.items()
        if score >= active_thresholds.get(category, 1.0)
    }
    allow = not violations
    return {
        "allow": allow,
        "reason": "allowed" if allow else "threshold_exceeded",
        "scores": scores,
        "thresholds": active_thresholds,
        "violations": violations,
        "provider": "openai",
        "model": OPENAI_MODEL,
    }
