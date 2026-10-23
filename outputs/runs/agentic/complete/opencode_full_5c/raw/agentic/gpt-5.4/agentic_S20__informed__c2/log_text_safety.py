from __future__ import annotations

import os

import requests


def check_log_text_safety(text: str) -> dict:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = payload.get("attributeScores", {})
    return {
        "provider": "Perspective API",
        "unsafe": any(
            scores.get(name, {}).get("summaryScore", {}).get("value", 0.0) >= 0.7
            for name in scores
        ),
        "scores": {
            name: scores.get(name, {}).get("summaryScore", {}).get("value")
            for name in scores
        },
        "raw": payload,
    }
