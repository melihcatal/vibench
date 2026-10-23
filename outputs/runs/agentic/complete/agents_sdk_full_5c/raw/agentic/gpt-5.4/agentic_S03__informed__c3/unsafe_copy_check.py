from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"



def unsafe_copy_check(text: str, language: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
    }
    body: Dict[str, Any] = {
        "comment": {"text": text},
        "requestedAttributes": requested_attributes,
        "doNotStore": True,
    }
    if language:
        body["languages"] = [language]
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=body,
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
        "flagged": any(score >= 0.7 for score in scores.values()),
        "raw": data,
    }
