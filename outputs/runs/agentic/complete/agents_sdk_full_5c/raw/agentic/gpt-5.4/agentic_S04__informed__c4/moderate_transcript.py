from __future__ import annotations

import os
from typing import Dict

import requests

from speech_models import ModerationResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_transcript(text: str) -> ModerationResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
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
        scores[key.lower()] = value["summaryScore"]["value"]
    flagged = any(score >= 0.7 for score in scores.values())
    return ModerationResult(flagged=flagged, scores=scores, raw=data)
