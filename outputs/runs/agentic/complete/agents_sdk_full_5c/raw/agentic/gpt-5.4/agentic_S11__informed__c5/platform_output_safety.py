from __future__ import annotations

import os
from typing import Any, Dict

import requests

from model_models import SafetyResult

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ("TOXICITY", "INSULT", "THREAT", "PROFANITY")


def check_platform_output_safety(text: str, language: str = "en") -> SafetyResult:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": [language],
            "requestedAttributes": {name: {} for name in DEFAULT_ATTRIBUTES},
        },
        timeout=30,
    )
    response.raise_for_status()
    payload: Dict[str, Any] = response.json()
    scores = {
        name: payload["attributeScores"][name]["summaryScore"]["value"]
        for name in DEFAULT_ATTRIBUTES
        if name in payload.get("attributeScores", {})
    }
    is_safe = max(scores.values(), default=0.0) < 0.7
    return SafetyResult(is_safe=is_safe, scores=scores, raw=payload)
