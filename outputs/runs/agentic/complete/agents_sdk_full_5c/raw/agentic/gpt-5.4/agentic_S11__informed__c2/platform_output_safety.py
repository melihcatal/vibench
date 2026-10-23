from __future__ import annotations

import os
from typing import Any, Dict

import requests

from model_models import SafetyResult

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ["TOXICITY", "INSULT", "THREAT", "PROFANITY"]


def check_platform_output_safety(text: str) -> SafetyResult:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {name: {} for name in DEFAULT_ATTRIBUTES},
        },
        timeout=30,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    scores = {
        name: data["attributeScores"][name]["summaryScore"]["value"]
        for name in DEFAULT_ATTRIBUTES
        if name in data.get("attributeScores", {})
    }
    safe = all(score < 0.7 for score in scores.values())
    return SafetyResult(safe=safe, scores=scores, raw=data)
