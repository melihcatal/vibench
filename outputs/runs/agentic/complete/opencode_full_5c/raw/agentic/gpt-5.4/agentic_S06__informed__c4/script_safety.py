from __future__ import annotations

import os

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_script_safety(text: str) -> dict:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
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
                "SEXUALLY_EXPLICIT": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        key: value["summaryScore"]["value"]
        for key, value in payload.get("attributeScores", {}).items()
    }
    return {
        "provider": "Perspective API",
        "scores": scores,
        "flagged": any(score >= 0.7 for score in scores.values()),
        "raw": payload,
    }
