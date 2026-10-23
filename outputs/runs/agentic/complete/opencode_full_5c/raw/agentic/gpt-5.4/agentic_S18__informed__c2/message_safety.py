from __future__ import annotations

import os
from typing import Dict

import requests

from messaging_models import SafetyResult, utc_now_iso


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_message_safety(source_message_id: str, text: str) -> SafetyResult:
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.getenv("PERSPECTIVE_API_KEY")},
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
    data = response.json()
    scores: Dict[str, float] = {
        name.lower(): values["summaryScore"]["value"]
        for name, values in data.get("attributeScores", {}).items()
    }
    flagged = any(score >= 0.7 for score in scores.values())
    return SafetyResult(
        provider="perspective-api",
        source_message_id=source_message_id,
        flagged=flagged,
        category_scores=scores,
        created_at=utc_now_iso(),
    )
