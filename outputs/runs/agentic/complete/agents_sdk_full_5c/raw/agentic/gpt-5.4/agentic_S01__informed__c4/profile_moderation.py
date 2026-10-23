from __future__ import annotations

import os
from typing import Dict, List

import requests

from identity_models import ModerationResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_ATTRIBUTES = {
    "TOXICITY": {},
    "SEVERE_TOXICITY": {},
    "INSULT": {},
    "PROFANITY": {},
    "THREAT": {},
}


def profile_moderation(profile_text: str, threshold: float = 0.8) -> ModerationResult:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    body = {
        "comment": {"text": profile_text},
        "requestedAttributes": PERSPECTIVE_ATTRIBUTES,
        "languages": ["en"],
    }
    response = requests.post(PERSPECTIVE_API_URL, params={"key": api_key}, json=body, timeout=30)
    response.raise_for_status()
    payload = response.json()

    attribute_scores = payload.get("attributeScores", {})
    risk_scores: Dict[str, float] = {}
    flagged_categories: List[str] = []
    for name, value in attribute_scores.items():
        score = float(value["summaryScore"]["value"])
        risk_scores[name.lower()] = score
        if score >= threshold:
            flagged_categories.append(name.lower())

    return ModerationResult(
        approved=not flagged_categories,
        provider="Perspective API",
        risk_scores=risk_scores,
        flagged_categories=flagged_categories,
        raw_response=payload,
    )
