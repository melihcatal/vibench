from __future__ import annotations

import os
from typing import Any, Dict

import requests


PROVIDER = "perspectiveapi"
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_message_safety(text: str) -> Dict[str, Any]:
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
    data = response.json()
    scores = {
        name.lower(): details["summaryScore"]["value"]
        for name, details in data.get("attributeScores", {}).items()
    }
    return {
        "provider": PROVIDER,
        "scores": scores,
        "unsafe": any(score >= 0.7 for score in scores.values()),
        "raw": data,
    }
