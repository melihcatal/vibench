from __future__ import annotations

import os
from typing import Dict

import requests

from messaging_models import SafetyAssessment


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_message_safety(text: str) -> SafetyAssessment:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Missing required environment variable: PERSPECTIVE_API_KEY")
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
            "languages": ["en"],
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json().get("attributeScores", {})
    category_scores: Dict[str, float] = {
        key.lower(): value["summaryScore"]["value"] for key, value in data.items()
    }
    max_score = max(category_scores.values(), default=0.0)
    return SafetyAssessment(
        safe=max_score < 0.7,
        blocked=max_score >= 0.7,
        category_scores=category_scores,
        provider="Perspective API",
    )
