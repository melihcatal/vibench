from __future__ import annotations

import os
from typing import Any, Dict, List

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ["TOXICITY", "INSULT", "THREAT", "PROFANITY"]


def check_ocr_safety(text: str, languages: List[str] | None = None) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Missing required environment variable: PERSPECTIVE_API_KEY")

    payload = {
        "comment": {"text": text},
        "languages": languages or ["en"],
        "requestedAttributes": {attribute: {} for attribute in DEFAULT_ATTRIBUTES},
        "doNotStore": True,
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
        "provider": "Perspective API",
        "scores": scores,
        "unsafe": any(score >= 0.7 for score in scores.values()),
        "response": data,
    }
