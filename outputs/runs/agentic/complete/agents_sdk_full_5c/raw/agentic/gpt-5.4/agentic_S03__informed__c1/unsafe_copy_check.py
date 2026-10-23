from __future__ import annotations

import os
from typing import Dict

import requests

from translation_models import SafetyCheckResult

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "THREAT", "PROFANITY"]


def unsafe_copy_check(text: str, language: str = "en", threshold: float = 0.8) -> SafetyCheckResult:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": [language],
            "requestedAttributes": {name: {} for name in DEFAULT_ATTRIBUTES},
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores: Dict[str, float] = {}
    for name, data in payload.get("attributeScores", {}).items():
        value = data.get("summaryScore", {}).get("value")
        if value is not None:
            scores[name] = float(value)
    is_safe = all(score < threshold for score in scores.values()) if scores else True
    return SafetyCheckResult(
        is_safe=is_safe,
        categories=scores,
        provider="Perspective API",
        raw=payload,
    )
