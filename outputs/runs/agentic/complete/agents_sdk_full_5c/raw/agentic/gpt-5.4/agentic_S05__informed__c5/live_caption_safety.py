from __future__ import annotations

import os

import requests

from speech_models import SafetyResult, normalize_text


PERSPECTIVE_API_KEY_ENV = "PERSPECTIVE_API_KEY"
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_live_caption_safety(text: str) -> SafetyResult:
    api_key = os.getenv(PERSPECTIVE_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Missing required environment variable: {PERSPECTIVE_API_KEY_ENV}")

    payload = {
        "comment": {"text": normalize_text(text)},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "PROFANITY": {},
        },
    }
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=payload,
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name.lower(): values["summaryScore"]["value"]
        for name, values in data.get("attributeScores", {}).items()
    }
    flagged = [name for name, score in scores.items() if score >= 0.7]
    return SafetyResult(unsafe=bool(flagged), flagged_categories=flagged, scores=scores, raw=data)
