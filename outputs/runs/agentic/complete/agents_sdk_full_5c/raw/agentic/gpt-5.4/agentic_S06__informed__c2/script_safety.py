from __future__ import annotations

import os
from typing import Dict

import requests

from speech_models import SafetyResult


PROVIDER = "perspective-api"
PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ("TOXICITY", "INSULT", "THREAT", "PROFANITY")


def check_script_safety(text: str, threshold: float = 0.8) -> SafetyResult:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    requested_attributes: Dict[str, dict] = {name: {} for name in DEFAULT_ATTRIBUTES}
    response = requests.post(
        PERSPECTIVE_URL,
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
        name: values["summaryScore"]["value"]
        for name, values in payload.get("attributeScores", {}).items()
    }
    blocked = any(score >= threshold for score in scores.values())
    return SafetyResult(blocked=blocked, provider=PROVIDER, categories=scores, raw=payload)
