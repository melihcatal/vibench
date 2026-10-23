from __future__ import annotations

import os
from typing import Dict

import requests

from identity_models import ModerationResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def profile_moderation(
    profile_text: str, toxicity_threshold: float = 0.7
) -> ModerationResult:
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": profile_text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json().get("attributeScores", {})
    scores: Dict[str, float] = {
        name.lower(): float(value["summaryScore"]["value"])
        for name, value in data.items()
    }
    flagged = [name for name, score in scores.items() if score >= toxicity_threshold]
    return ModerationResult(
        allowed=not flagged,
        category_scores=scores,
        flagged_categories=flagged,
    )
