from __future__ import annotations

import os
from typing import Dict, Iterable

import requests

from speech_models import SafetyResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ("TOXICITY", "INSULT", "PROFANITY", "THREAT")


def check_script_safety(text: str, attributes: Iterable[str] = DEFAULT_ATTRIBUTES, threshold: float = 0.75) -> SafetyResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise EnvironmentError("PERSPECTIVE_API_KEY is required for Perspective API.")
    requested = {attribute: {} for attribute in attributes}
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "requestedAttributes": requested,
            "languages": ["en"],
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores: Dict[str, float] = {}
    flagged = []
    for name, detail in payload.get("attributeScores", {}).items():
        value = float(detail["summaryScore"]["value"])
        scores[name] = value
        if value >= threshold:
            flagged.append(name)
    return SafetyResult(
        safe=not flagged,
        scores=scores,
        flagged_categories=flagged,
        provider="perspectiveapi",
    )
