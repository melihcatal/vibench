from __future__ import annotations

import os
from typing import Any, Dict

import requests


def metric_annotation_safety(text: str, language: str = "en") -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
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
        name.lower(): value["summaryScore"]["value"]
        for name, value in data.get("attributeScores", {}).items()
    }
    return {
        "provider": "perspective-api",
        "host": "commentanalyzer.googleapis.com",
        "text": text,
        "scores": scores,
        "unsafe": any(score >= 0.7 for score in scores.values()),
    }
