from __future__ import annotations

import os
from typing import Any, Dict

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def vendor_text_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")

    response = requests.post(
        PERSPECTIVE_API_URL,
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
    data = response.json()
    scores = {
        name.lower(): payload["summaryScore"]["value"]
        for name, payload in data.get("attributeScores", {}).items()
    }
    return {
        "provider": "Perspective API",
        "scores": scores,
        "flagged": any(score >= 0.7 for score in scores.values()),
    }
