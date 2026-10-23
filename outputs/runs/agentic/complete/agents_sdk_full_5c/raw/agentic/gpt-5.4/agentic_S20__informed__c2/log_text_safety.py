from __future__ import annotations

import os
from typing import Dict

import requests

from observability_models import SafetyCheckResult

PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"



def log_text_safety(text: str) -> SafetyCheckResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    response = requests.post(
        PERSPECTIVE_API_HOST,
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
    data = response.json()
    scores: Dict[str, float] = {
        name: details["summaryScore"]["value"]
        for name, details in data.get("attributeScores", {}).items()
    }
    flagged = any(score >= 0.7 for score in scores.values())
    return SafetyCheckResult(
        flagged=flagged,
        category_scores=scores,
        provider="Perspective API",
        raw=data,
    )
