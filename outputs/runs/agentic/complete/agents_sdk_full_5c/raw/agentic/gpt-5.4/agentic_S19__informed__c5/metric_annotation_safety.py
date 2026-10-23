from __future__ import annotations

import os
from typing import Any, Dict

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"



def metric_annotation_safety(text: str, languages: list[str] | None = None) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    payload = {
        "comment": {"text": text},
        "languages": languages or ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "PROFANITY": {},
        },
    }
    response = requests.post(PERSPECTIVE_API_URL, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    scores = {
        name: values["summaryScore"]["value"]
        for name, values in data.get("attributeScores", {}).items()
    }
    max_score = max(scores.values()) if scores else 0.0
    return {
        "provider": "Perspective API",
        "endpoint": PERSPECTIVE_API_URL,
        "scores": scores,
        "unsafe": max_score >= 0.7,
    }
