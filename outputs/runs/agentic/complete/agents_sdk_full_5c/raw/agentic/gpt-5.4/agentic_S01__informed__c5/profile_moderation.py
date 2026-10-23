from __future__ import annotations

import os
from typing import Dict

import requests

from identity_models import ModerationResult


PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def profile_moderation(text: str, threshold: float = 0.75) -> ModerationResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing required environment variable: PERSPECTIVE_API_KEY")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "PROFANITY": {},
        },
    }
    response = requests.post(
        PERSPECTIVE_ENDPOINT,
        params={"key": api_key},
        json=payload,
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    scores: Dict[str, float] = {}
    for name, value in data.get("attributeScores", {}).items():
        score = float(value["summaryScore"]["value"])
        scores[name.lower()] = score
    flagged = any(score >= threshold for score in scores.values())
    return ModerationResult(
        allowed=not flagged,
        provider="perspective_api",
        flagged=flagged,
        scores=scores,
        normalized_text=text.strip(),
    )
