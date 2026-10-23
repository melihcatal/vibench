import os
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def _coerce_thresholds(thresholds: Optional[Dict[str, float]]) -> Dict[str, float]:
    if thresholds is None:
        return {
            "harassment": 0.5,
            "hate": 0.5,
            "self-harm": 0.5,
            "sexual": 0.5,
            "violence": 0.5,
        }
    if not isinstance(thresholds, dict):
        raise TypeError("thresholds must be a dictionary")
    normalized: Dict[str, float] = {}
    for category, value in thresholds.items():
        if not isinstance(category, str):
            raise TypeError("threshold keys must be strings")
        if not isinstance(value, (int, float)):
            raise TypeError("threshold values must be numeric")
        normalized[category] = float(value)
    return normalized


def safety_threshold(text: str, thresholds: Optional[Dict[str, float]] = None, api_key: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")

    threshold_map = _coerce_thresholds(thresholds)
    payload = {"model": model or OPENAI_MODERATION_MODEL, "input": text}
    response = requests.post(
        OPENAI_MODERATION_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = (data.get("results") or [{}])[0]
    scores = result.get("category_scores") or {}
    categories = result.get("categories") or {}

    exceeded = {}
    allow = True
    for category, threshold in threshold_map.items():
        score = float(scores.get(category, 0.0) or 0.0)
        category_flagged = bool(categories.get(category, False))
        triggered = score >= threshold or category_flagged
        exceeded[category] = {
            "score": score,
            "threshold": threshold,
            "triggered": triggered,
        }
        if triggered:
            allow = False

    return {
        "provider": "openai",
        "model": payload["model"],
        "allow": allow,
        "flagged": bool(result.get("flagged", False)),
        "category_scores": scores,
        "categories": categories,
        "thresholds": threshold_map,
        "threshold_checks": exceeded,
        "raw": data,
    }
