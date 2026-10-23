from __future__ import annotations

import os

import requests


def check_message_safety(text: str) -> dict:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
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
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name.lower(): value["summaryScore"]["value"]
        for name, value in data.get("attributeScores", {}).items()
    }
    return {
        "provider": "perspective-api",
        "endpoint": "commentanalyzer.googleapis.com",
        "scores": scores,
        "flagged": any(score >= 0.8 for score in scores.values()),
    }
