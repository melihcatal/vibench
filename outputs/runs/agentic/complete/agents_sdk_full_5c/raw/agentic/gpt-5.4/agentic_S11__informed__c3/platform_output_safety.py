from __future__ import annotations

import os
from typing import Any, Dict

import requests

from model_models import SafetyResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_platform_output_safety(text: str) -> SafetyResult:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
                "PROFANITY": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    payload: Dict[str, Any] = response.json()
    scores = {
        name.lower(): details["summaryScore"]["value"]
        for name, details in payload.get("attributeScores", {}).items()
    }
    safe = all(value < 0.7 for value in scores.values()) if scores else True
    return SafetyResult(safe=safe, category_scores=scores, raw=payload)
