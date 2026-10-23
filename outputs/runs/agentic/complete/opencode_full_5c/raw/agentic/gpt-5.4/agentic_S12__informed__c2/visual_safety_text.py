from __future__ import annotations

import os

import requests

from vision_models import TextSafetyResult


def visual_safety_text(text: str, threshold: float = 0.7) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
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
    scores = {
        name.lower(): attribute.get("summaryScore", {}).get("value", 0.0)
        for name, attribute in payload.get("attributeScores", {}).items()
    }
    result = TextSafetyResult(
        provider="perspective-api",
        safe=all(value < threshold for value in scores.values()),
        scores=scores,
        raw_response=payload,
    )
    return result.to_dict()
