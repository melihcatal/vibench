from __future__ import annotations

import os
from typing import Dict

import requests

from translation_models import SafetyCheckResult


PERSPECTIVE_PROVIDER = "Perspective API"
PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_ATTRIBUTES = [
    "TOXICITY",
    "INSULT",
    "THREAT",
    "PROFANITY",
    "IDENTITY_ATTACK",
]


def check_unsafe_copy(
    text: str, language: str | None = None, threshold: float = 0.75
) -> SafetyCheckResult:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    payload: Dict[str, object] = {
        "comment": {"text": text},
        "requestedAttributes": {name: {} for name in PERSPECTIVE_ATTRIBUTES},
        "doNotStore": True,
    }
    if language:
        payload["languages"] = [language]
    response = requests.post(
        PERSPECTIVE_URL,
        params={"key": api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    attribute_scores = data.get("attributeScores", {})
    scores = {
        key.lower(): float(value["summaryScore"]["value"])
        for key, value in attribute_scores.items()
        if "summaryScore" in value
    }
    flagged_categories = [name for name, score in scores.items() if score >= threshold]
    return SafetyCheckResult(
        is_safe=not flagged_categories,
        flagged_categories=flagged_categories,
        scores=scores,
        provider=PERSPECTIVE_PROVIDER,
        raw_response=data,
    )
