from __future__ import annotations

import os
from typing import Any, Dict

import requests


PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_vendor_text(text: str) -> Dict[str, Any]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        PERSPECTIVE_ENDPOINT,
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
        name.lower(): details["summaryScore"]["value"]
        for name, details in payload.get("attributeScores", {}).items()
    }
    return {
        "provider": "perspective-api",
        "scores": scores,
        "flagged": any(score >= 0.7 for score in scores.values()),
        "raw_response": payload,
    }
