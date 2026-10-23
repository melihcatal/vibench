from __future__ import annotations

import os

import requests

from speech_models import SafetyResult, first_text


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_script_safety(script: str, threshold: float = 0.7) -> SafetyResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing required environment variable: PERSPECTIVE_API_KEY")
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": first_text(script)},
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
    data = response.json()["attributeScores"]
    scores = {
        name.lower(): value["summaryScore"]["value"] for name, value in data.items()
    }
    return SafetyResult(
        flagged=any(score >= threshold for score in scores.values()),
        category_scores=scores,
    )
