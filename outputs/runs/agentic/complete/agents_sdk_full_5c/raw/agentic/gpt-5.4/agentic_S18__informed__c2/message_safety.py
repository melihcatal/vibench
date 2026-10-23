from __future__ import annotations

import os
from typing import Any, Dict

import requests

from messaging_models import SafetyAssessment


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_message_safety(text: str, *, language: str = "en") -> SafetyAssessment:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": [language],
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
            },
        },
        timeout=20,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    scores = {
        name.lower(): payload["summaryScore"]["value"]
        for name, payload in data.get("attributeScores", {}).items()
    }
    flagged = any(value >= 0.8 for value in scores.values())
    return SafetyAssessment(flagged=flagged, risk_scores=scores, provider="Perspective API", details=data)
