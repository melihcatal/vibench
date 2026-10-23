from __future__ import annotations

import os

import requests

from identity_models import ModerationResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_claim_text(text: str, threshold: float = 0.7) -> ModerationResult:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "PROFANITY": {},
        },
        "languages": ["en"],
    }
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=payload,
        timeout=20,
    )
    response.raise_for_status()
    raw = response.json()
    scores = {
        name.lower(): details["summaryScore"]["value"]
        for name, details in raw.get("attributeScores", {}).items()
    }
    risk_score = max(scores.values(), default=0.0)
    flagged = risk_score >= threshold
    return ModerationResult(
        allowed=not flagged,
        flagged=flagged,
        risk_score=risk_score,
        categories=scores,
        provider="Perspective API",
        raw=raw,
    )
