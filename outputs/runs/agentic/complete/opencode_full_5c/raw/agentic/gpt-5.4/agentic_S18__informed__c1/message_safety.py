from __future__ import annotations

import requests


def check_message_safety(text: str) -> dict:
    api_key = __import__("os").getenv("PERSPECTIVE_API_KEY")
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
        key.lower(): value["summaryScore"]["value"]
        for key, value in data.get("attributeScores", {}).items()
    }
    return {
        "provider": "perspective_api",
        "scores": scores,
        "unsafe": any(score >= 0.7 for score in scores.values()),
    }
