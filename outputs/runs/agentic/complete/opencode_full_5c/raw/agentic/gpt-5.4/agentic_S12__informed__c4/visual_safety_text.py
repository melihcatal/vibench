from __future__ import annotations

import os

import requests


def visual_safety_text(text: str, threshold: float = 0.7) -> dict:
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    response = requests.post(
        url,
        params={"key": os.getenv("PERSPECTIVE_API_KEY")},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    score = payload["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return {
        "provider": "perspective-api",
        "unsafe": score >= threshold,
        "toxicity": score,
        "raw_response": payload,
    }
