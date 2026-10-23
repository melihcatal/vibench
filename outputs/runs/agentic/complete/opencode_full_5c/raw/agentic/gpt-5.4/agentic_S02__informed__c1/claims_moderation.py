from __future__ import annotations

import os

import requests


def moderate_claim_text(text: str) -> dict:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    response = requests.post(
        url,
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
    payload = response.json()
    scores = payload.get("attributeScores", {})
    return {
        "provider": "Perspective API",
        "scores": {
            name.lower(): details["summaryScore"]["value"]
            for name, details in scores.items()
        },
        "raw": payload,
    }
