from __future__ import annotations

import os
from typing import Dict

import requests

from speech_models import SafetyResult, ensure_text


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_script_safety(text: str, languages: list[str] | None = None) -> SafetyResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise EnvironmentError("PERSPECTIVE_API_KEY is required for Perspective API")
    requested_text = ensure_text(text, "text")
    payload = {
        "comment": {"text": requested_text},
        "languages": languages or ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores: Dict[str, float] = {}
    for key, value in data.get("attributeScores", {}).items():
        summary = value.get("summaryScore", {})
        score_value = summary.get("value")
        if score_value is not None:
            scores[key.lower()] = float(score_value)
    flagged = any(score >= 0.8 for score in scores.values())
    return SafetyResult(provider="perspective-api", flagged=flagged, scores=scores, raw=data)
