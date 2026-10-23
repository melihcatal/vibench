from __future__ import annotations

import os
from typing import Dict

import requests

from model_models import SafetyCheckResult

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ("TOXICITY", "INSULT", "THREAT", "PROFANITY")


def check_text_safety(text: str, language: str = "en") -> SafetyCheckResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")

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
    data = response.json()
    scores: Dict[str, float] = {
        name: data["attributeScores"][name]["summaryScore"]["value"]
        for name in DEFAULT_ATTRIBUTES
        if name in data.get("attributeScores", {})
    }
    flagged = any(value >= 0.7 for value in scores.values())
    return SafetyCheckResult(provider="perspective", flagged=flagged, scores=scores, raw=data)
