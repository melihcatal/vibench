from __future__ import annotations

import os
from typing import Any, Dict

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_vendor_text(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Missing required environment variable: PERSPECTIVE_API_KEY")
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
            "languages": ["en"],
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = data.get("attributeScores", {})
    return {
        "provider": "perspective-api",
        "scores": {
            name.lower(): scores.get(name, {}).get("summaryScore", {}).get("value", 0.0)
            for name in ["TOXICITY", "INSULT", "THREAT"]
        },
        "flagged": any(
            scores.get(name, {}).get("summaryScore", {}).get("value", 0.0) >= 0.7
            for name in ["TOXICITY", "INSULT", "THREAT"]
        ),
    }
