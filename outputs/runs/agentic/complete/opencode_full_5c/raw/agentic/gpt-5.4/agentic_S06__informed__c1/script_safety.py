from __future__ import annotations

import os

import requests

from speech_models import SafetyResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_script_safety(text: str, threshold: float = 0.8) -> SafetyResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise EnvironmentError("PERSPECTIVE_API_KEY is required")
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
                "PROFANITY": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        key.lower(): value["summaryScore"]["value"]
        for key, value in data.get("attributeScores", {}).items()
    }
    blocked = any(score >= threshold for score in scores.values())
    return SafetyResult(
        provider="perspective", blocked=blocked, scores=scores, raw=data
    )
