from __future__ import annotations

import json

import requests

PROVIDER = "Perspective API"
PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def payload_safety(text: str, api_key: str | None = None) -> str:
    params = {"key": api_key or ""}
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}},
    }
    response = requests.post(PERSPECTIVE_URL, params=params, json=data, timeout=20)
    response.raise_for_status()
    return json.dumps({"provider": PROVIDER, "scores": response.json().get("attributeScores", {})})
