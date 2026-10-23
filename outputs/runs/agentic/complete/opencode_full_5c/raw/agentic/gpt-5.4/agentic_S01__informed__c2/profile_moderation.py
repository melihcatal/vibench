from __future__ import annotations

import os

import requests

from identity_models import ModerationResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def profile_moderation(text: str, toxicity_threshold: float = 0.7) -> ModerationResult:
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
            },
            "languages": ["en"],
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        category: details["summaryScore"]["value"]
        for category, details in payload.get("attributeScores", {}).items()
    }
    flagged = [
        category for category, value in scores.items() if value >= toxicity_threshold
    ]
    return ModerationResult(
        approved=not flagged,
        provider="perspective_api",
        scores=scores,
        flagged_categories=flagged,
        raw_response=payload,
    )
