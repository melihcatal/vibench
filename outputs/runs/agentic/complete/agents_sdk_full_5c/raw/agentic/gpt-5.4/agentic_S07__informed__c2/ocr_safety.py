from __future__ import annotations

import os
from typing import Any, Dict

import requests

from document_models import normalize_text

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_ocr_safety(text: str, languages: list[str] | None = None) -> Dict[str, Any]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")

    payload = {
        "comment": {"text": normalize_text(text)},
        "languages": languages or ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "PROFANITY": {},
        },
    }
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name: details["summaryScore"]["value"]
        for name, details in data.get("attributeScores", {}).items()
    }
    return {
        "provider": "perspective-api",
        "endpoint": PERSPECTIVE_API_URL,
        "scores": scores,
        "flagged": any(score >= 0.7 for score in scores.values()),
        "raw": data,
    }
