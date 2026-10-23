from __future__ import annotations

import os
from typing import Any, Dict

import requests

from identity_models import ModerationResult


PROVIDER = "Perspective API"
PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"



def moderate_claim_text(text: str, language: str = "en") -> ModerationResult:
    response = requests.post(
        PERSPECTIVE_URL,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": text},
            "languages": [language],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    payload: Dict[str, Any] = response.json()
    attributes = payload.get("attributeScores", {})
    scores = {
        name.lower(): float(value["summaryScore"]["value"])
        for name, value in attributes.items()
        if "summaryScore" in value
    }
    max_score = max(scores.values(), default=0.0)
    return ModerationResult(
        provider=PROVIDER,
        action="block" if max_score >= 0.85 else "review" if max_score >= 0.6 else "allow",
        flagged=max_score >= 0.6,
        scores=scores,
        raw=payload,
    )
