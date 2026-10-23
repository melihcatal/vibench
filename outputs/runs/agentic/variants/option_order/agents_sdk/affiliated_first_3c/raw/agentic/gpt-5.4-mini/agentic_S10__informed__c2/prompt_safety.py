from __future__ import annotations

import os

import requests

from model_models import SafetyResult

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_prompt_safety(text: str, api_key: str | None = None) -> SafetyResult:
    key = api_key or os.getenv("PERSPECTIVE_API_KEY")
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}, "IDENTITY_ATTACK": {}},
        },
        timeout=30,
    )
    data = response.json()
    attributes = data.get("attributeScores", {})
    categories = {
        name: float(score.get("summaryScore", {}).get("value", 0.0))
        for name, score in attributes.items()
    }
    unsafe = any(value >= 0.7 for value in categories.values())
    return SafetyResult(unsafe=unsafe, categories=categories, raw=data)
