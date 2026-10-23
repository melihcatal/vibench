from __future__ import annotations

import os
from typing import Any

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_corpus_text(text: str, *, threshold: float = 0.8) -> dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
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
    scores = {
        name.lower(): values["summaryScore"]["value"]
        for name, values in payload.get("attributeScores", {}).items()
    }
    flagged = any(score >= threshold for score in scores.values())
    return {
        "provider": "Perspective API",
        "flagged": flagged,
        "threshold": threshold,
        "scores": scores,
    }
