from __future__ import annotations

import os
from typing import Any, Dict

import requests

from identity_models import ModerationResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_claim_text(text: str, language: str = "en") -> ModerationResult:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    payload: Dict[str, Any] = {
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
    categories = {
        name.lower(): float(details["summaryScore"]["value"])
        for name, details in data.get("attributeScores", {}).items()
    }
    flagged = any(score >= 0.7 for score in categories.values())
    return ModerationResult(
        flagged=flagged,
        categories=categories,
        provider="perspective_api",
        raw=data,
    )
