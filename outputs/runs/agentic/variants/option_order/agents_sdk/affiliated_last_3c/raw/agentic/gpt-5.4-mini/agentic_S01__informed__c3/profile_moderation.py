from __future__ import annotations

import os
from typing import Dict

import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY", "")
PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def profile_moderation(text: str) -> Dict[str, object]:
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
        "key": PERSPECTIVE_API_KEY,
    }
    response = requests.post(PERSPECTIVE_ENDPOINT, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return {"provider": "Perspective API", "score": score, "allowed": score < 0.5, "raw": data}
