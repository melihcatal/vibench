from __future__ import annotations

import os

import requests


def moderate_claim_text(text: str, language: str = "en") -> dict:
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": text},
            "languages": [language],
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
        "provider": "Perspective API",
        "endpoint": "commentanalyzer.googleapis.com",
        "scores": scores,
        "raw": data,
    }
