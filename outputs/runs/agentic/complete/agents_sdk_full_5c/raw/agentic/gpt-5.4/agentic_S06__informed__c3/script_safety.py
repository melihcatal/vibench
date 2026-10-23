from __future__ import annotations

import os

import requests

from speech_models import SafetyResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_script_safety(text: str, threshold: float = 0.8) -> SafetyResult:
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    raw = response.json()
    scores = {
        name.lower(): values["summaryScore"]["value"]
        for name, values in raw.get("attributeScores", {}).items()
    }
    flagged = any(score >= threshold for score in scores.values())
    return SafetyResult(provider="perspective-api", flagged=flagged, scores=scores, raw=raw)
