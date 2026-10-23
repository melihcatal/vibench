from __future__ import annotations

import os

import requests

from speech_models import SafetyResult


PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_ENV = "PERSPECTIVE_API_KEY"


def check_live_caption_safety(text: str) -> SafetyResult:
    api_key = os.getenv(PERSPECTIVE_API_ENV)
    if not api_key:
        raise RuntimeError(f"Missing required environment variable: {PERSPECTIVE_API_ENV}")
    response = requests.post(
        PERSPECTIVE_API_HOST,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
            },
        },
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name.lower(): payload["summaryScore"]["value"]
        for name, payload in data.get("attributeScores", {}).items()
    }
    return SafetyResult(
        is_unsafe=any(score >= 0.8 for score in scores.values()),
        scores=scores,
        raw=data,
    )
