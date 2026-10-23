from __future__ import annotations

import os
from typing import Dict

import requests

from translation_models import SafetyCheckResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ["TOXICITY", "INSULT", "THREAT", "PROFANITY", "IDENTITY_ATTACK"]


def unsafe_copy_check(text: str, language: str = "en") -> SafetyCheckResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY must be set")

    payload = {
        "comment": {"text": text},
        "languages": [language],
        "requestedAttributes": {attribute: {} for attribute in DEFAULT_ATTRIBUTES},
    }
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores: Dict[str, float] = {
        name: details["summaryScore"]["value"]
        for name, details in data.get("attributeScores", {}).items()
    }
    flagged = any(score >= 0.7 for score in scores.values())
    return SafetyCheckResult(flagged=flagged, scores=scores, provider="perspectiveapi", raw=data)
