from __future__ import annotations

import os
from typing import Any, Dict

import requests


PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_message_safety(text: str, language: str = "en") -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Missing required environment variable: PERSPECTIVE_API_KEY")
    response = requests.post(
        PERSPECTIVE_ENDPOINT,
        params={"key": api_key},
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
        name.lower(): details["summaryScore"]["value"]
        for name, details in data.get("attributeScores", {}).items()
    }
    return {
        "provider": "perspective_api",
        "scores": scores,
        "flagged": any(score >= 0.8 for score in scores.values()),
        "raw": data,
    }
