from __future__ import annotations

import os
from typing import Dict

from security_client import get_perspective_session
from security_models import PayloadSafetyResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def payload_safety(text: str) -> PayloadSafetyResult:
    session = get_perspective_session()
    response = session.post(
        PERSPECTIVE_API_URL,
        params={"key": os.getenv("PERSPECTIVE_API_KEY")},
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
    data = response.json().get("attributeScores", {})
    scores: Dict[str, float] = {
        name.lower(): float(details["summaryScore"]["value"])
        for name, details in data.items()
    }
    categories = [name for name, value in scores.items() if value >= 0.7]
    return PayloadSafetyResult(
        provider="Perspective API",
        flagged=bool(categories),
        scores=scores,
        categories=categories,
    )
