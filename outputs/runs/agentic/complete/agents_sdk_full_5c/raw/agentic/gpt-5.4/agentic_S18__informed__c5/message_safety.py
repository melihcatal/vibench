from __future__ import annotations

import os
from typing import Any, Dict

import requests


PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_message_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Missing PERSPECTIVE_API_KEY")

    response = requests.post(
        f"{PERSPECTIVE_API_HOST}?key={api_key}",
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
            },
        },
        timeout=20,
    )
    response.raise_for_status()
    body = response.json()
    scores = {
        name.lower(): values["summaryScore"]["value"]
        for name, values in body.get("attributeScores", {}).items()
    }
    return {
        "provider": "perspective-api",
        "scores": scores,
        "flagged": any(score >= 0.8 for score in scores.values()),
        "raw": body,
    }
