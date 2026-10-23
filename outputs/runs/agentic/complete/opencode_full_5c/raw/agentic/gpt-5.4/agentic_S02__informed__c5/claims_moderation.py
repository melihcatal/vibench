from __future__ import annotations

import os
from typing import Any, Dict

import requests


def moderate_claims_text(text: str) -> Dict[str, Any]:
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
                "PROFANITY": {},
                "THREAT": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    attribute_scores = data.get("attributeScores", {})
    return {
        "provider": "Perspective API",
        "scores": {
            key: value.get("summaryScore", {}).get("value")
            for key, value in attribute_scores.items()
        },
        "raw": data,
    }
