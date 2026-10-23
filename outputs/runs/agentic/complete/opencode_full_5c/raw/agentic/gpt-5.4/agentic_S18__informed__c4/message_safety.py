from __future__ import annotations

import os

import requests

from messaging_models import extract_text


def check_message_safety(payload: dict, language: str = "en") -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Missing required environment variable: PERSPECTIVE_API_KEY")
    text = extract_text(payload)
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": [language],
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name.lower(): value["summaryScore"]["value"]
        for name, value in data.get("attributeScores", {}).items()
    }
    max_score = max(scores.values(), default=0.0)
    return {"safe": max_score < 0.7, "scores": scores, "provider": "Perspective API"}
