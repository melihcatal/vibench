from __future__ import annotations

import os
from typing import Dict

import requests

from identity_models import ModerationResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"



def moderate_claim_text(text: str) -> ModerationResult:
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
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores: Dict[str, float] = {}
    for name, details in payload.get("attributeScores", {}).items():
        value = details.get("summaryScore", {}).get("value")
        if value is not None:
            scores[name.lower()] = float(value)
    flagged = any(score >= 0.7 for score in scores.values())
    return ModerationResult(
        provider="Perspective API",
        flagged=flagged,
        category_scores=scores,
        raw=payload,
    )
