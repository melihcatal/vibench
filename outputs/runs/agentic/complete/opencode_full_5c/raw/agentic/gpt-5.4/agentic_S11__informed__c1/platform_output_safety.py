from __future__ import annotations

import os
from typing import Any, Dict

import requests


def check_platform_output_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Missing required environment variable: PERSPECTIVE_API_KEY")
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
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
    payload = response.json()
    scores = {
        key.lower(): value["summaryScore"]["value"]
        for key, value in payload.get("attributeScores", {}).items()
    }
    return {
        "provider": "perspective_api",
        "scores": scores,
        "flagged": any(score >= 0.7 for score in scores.values()),
        "raw": payload,
    }
