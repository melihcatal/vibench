from __future__ import annotations

import os
from typing import Any

import requests


def check_record_text_safety(text: str) -> dict[str, Any]:
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
                "THREAT": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name.lower(): value["summaryScore"]["value"]
        for name, value in data.get("attributeScores", {}).items()
    }
    return {
        "provider": "Perspective API",
        "scores": scores,
        "flagged": any(score >= 0.7 for score in scores.values()),
    }
