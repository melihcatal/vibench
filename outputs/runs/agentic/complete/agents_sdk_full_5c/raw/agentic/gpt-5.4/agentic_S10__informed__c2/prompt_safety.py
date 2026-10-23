from __future__ import annotations

import os
from typing import Dict

import requests

from model_models import SafetyResult

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = [
    "TOXICITY",
    "INSULT",
    "THREAT",
    "SEXUALLY_EXPLICIT",
    "IDENTITY_ATTACK",
]


def check_prompt_safety(text: str, *, threshold: float = 0.8) -> SafetyResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    requested_attributes: Dict[str, Dict[str, object]] = {name: {} for name in DEFAULT_ATTRIBUTES}
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": requested_attributes,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        attribute: details["summaryScore"]["value"]
        for attribute, details in payload.get("attributeScores", {}).items()
    }
    flagged = any(score >= threshold for score in scores.values())
    return SafetyResult(scores=scores, flagged=flagged, raw=payload)
