from __future__ import annotations

from typing import Dict

import requests

PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def profile_moderation(text: str) -> Dict[str, object]:
    key = __import__("os").environ.get("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "PROFANITY": {}, "SEVERE_TOXICITY": {}},
    }
    response = requests.post(f"{PERSPECTIVE_API_HOST}?key={key}", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    scores = data.get("attributeScores", {})
    return {"provider": "Perspective API", "scores": scores, "raw": data}
