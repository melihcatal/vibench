from __future__ import annotations

import os
from typing import Any, Dict

import requests

from identity_models import normalize_profile_text


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def profile_moderation(profile_text: str, language: str = "en") -> Dict[str, Any]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    text = normalize_profile_text(profile_text)
    payload = {
        "comment": {"text": text},
        "languages": [language],
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
        name.lower(): attr["summaryScore"]["value"]
        for name, attr in data.get("attributeScores", {}).items()
    }
    max_score = max(scores.values()) if scores else 0.0
    return {
        "provider": "Perspective API",
        "text": text,
        "scores": scores,
        "flagged": max_score >= 0.7,
    }
