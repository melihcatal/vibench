from __future__ import annotations

import os

import requests


def moderate_vendor_text(text: str) -> dict:
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
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
    scores = {
        key.lower(): value["summaryScore"]["value"]
        for key, value in payload.get("attributeScores", {}).items()
    }
    flagged = any(score >= 0.7 for score in scores.values())
    return {
        "provider": "Perspective API",
        "flagged": flagged,
        "scores": scores,
        "raw_response": payload,
    }
