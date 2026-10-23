from __future__ import annotations

import os
from typing import Dict

import requests

from speech_models import SafetyResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_ATTRIBUTES = ["TOXICITY", "INSULT", "PROFANITY", "THREAT"]


def check_script_safety(text: str, language: str = "en") -> SafetyResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Missing PERSPECTIVE_API_KEY")

    payload = {
        "comment": {"text": text},
        "languages": [language],
        "requestedAttributes": {name: {} for name in PERSPECTIVE_ATTRIBUTES},
    }
    response = requests.post(PERSPECTIVE_API_URL, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    scores: Dict[str, float] = {}
    for attr, value in data.get("attributeScores", {}).items():
        scores[attr.lower()] = value["summaryScore"]["value"]
    flagged = any(score >= 0.7 for score in scores.values())
    return SafetyResult(provider="Perspective API", flagged=flagged, scores=scores, raw=data)
