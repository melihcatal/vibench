from __future__ import annotations

import os
from typing import Dict

import requests

from translation_models import SafetyCheckResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_localized_copy(
    text: str, language: str | None = None, threshold: float = 0.7
) -> SafetyCheckResult:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    requested_attributes: Dict[str, Dict] = {
        "TOXICITY": {},
        "INSULT": {},
        "THREAT": {},
        "PROFANITY": {},
        "SEXUALLY_EXPLICIT": {},
    }
    payload = {
        "comment": {"text": text},
        "requestedAttributes": requested_attributes,
        "languages": [language] if language else None,
        "doNotStore": True,
    }
    payload = {key: value for key, value in payload.items() if value is not None}
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name.lower(): details["summaryScore"]["value"]
        for name, details in data.get("attributeScores", {}).items()
    }
    flagged = [name for name, score in scores.items() if score >= threshold]
    return SafetyCheckResult(
        unsafe=bool(flagged),
        category_scores=scores,
        flagged_categories=flagged,
        raw=data,
    )
