from __future__ import annotations

import os
from typing import Any, Dict

import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY", "")
PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def profile_moderation(text: str) -> Dict[str, Any]:
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        "doNotStore": True,
        "languages": ["en"],
    }
    response = requests.post(PERSPECTIVE_ENDPOINT, params={"key": PERSPECTIVE_API_KEY}, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    scores = {name.lower(): value["summaryScore"]["value"] for name, value in data.get("attributeScores", {}).items()}
    return {"provider": "perspective", "scores": scores, "raw": data}
