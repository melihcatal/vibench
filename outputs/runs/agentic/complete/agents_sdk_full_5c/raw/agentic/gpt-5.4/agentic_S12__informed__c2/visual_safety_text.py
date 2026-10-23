from __future__ import annotations

import os
from typing import Dict, Any

import requests

PERSPECTIVE_PROVIDER = "perspective-api"
PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def visual_safety_text(text: str) -> Dict[str, Any]:
    response = requests.post(
        PERSPECTIVE_URL,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
                "PROFANITY": {},
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
        "provider": PERSPECTIVE_PROVIDER,
        "endpoint": PERSPECTIVE_URL,
        "scores": scores,
        "raw_response": data,
    }
