from __future__ import annotations

import os

import requests


def claims_moderation(text: str, languages: list[str] | None = None) -> dict:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": languages or ["en"],
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
        name.lower(): details["summaryScore"]["value"]
        for name, details in data.get("attributeScores", {}).items()
    }
    return {
        "provider": "perspective_api",
        "scores": scores,
        "flagged": any(score >= 0.8 for score in scores.values()),
        "raw": data,
    }
