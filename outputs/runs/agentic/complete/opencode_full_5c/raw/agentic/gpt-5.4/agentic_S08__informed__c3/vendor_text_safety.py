from __future__ import annotations

import os
from typing import Any, Dict

import requests


def moderate_vendor_text(text: str, language: str = "en") -> Dict[str, Any]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
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
    payload = response.json()
    scores = {
        name.lower(): attribute["summaryScore"]["value"]
        for name, attribute in payload.get("attributeScores", {}).items()
    }
    return {
        "provider": "perspective-api",
        "scores": scores,
        "flagged": any(score >= 0.7 for score in scores.values()),
        "raw_response": payload,
    }
