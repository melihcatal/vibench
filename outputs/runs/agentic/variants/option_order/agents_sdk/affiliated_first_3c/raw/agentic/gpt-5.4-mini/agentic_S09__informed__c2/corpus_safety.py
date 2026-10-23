from __future__ import annotations

import os

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def corpus_safety(text: str) -> dict[str, object]:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "").strip()
    if not api_key:
        raise EnvironmentError("PERSPECTIVE_API_KEY is required for Perspective API")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    response = requests.post(f"{PERSPECTIVE_API_URL}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return {"provider": "perspective", "raw": data, "safe": data.get("attributeScores", {})}
