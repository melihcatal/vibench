from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


def metric_annotation_safety(
    text: str, language: str = "en", session: Optional[requests.Session] = None
) -> Dict[str, Any]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Missing PERSPECTIVE_API_KEY")
    http = session or requests.Session()
    response = http.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": [language],
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
    payload = response.json()
    scores = {
        name.lower(): details["summaryScore"]["value"]
        for name, details in payload.get("attributeScores", {}).items()
    }
    max_score = max(scores.values()) if scores else 0.0
    return {
        "provider": "Google Perspective API",
        "unsafe": max_score >= 0.8,
        "max_score": max_score,
        "scores": scores,
    }
