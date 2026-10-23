from __future__ import annotations

import os
from typing import Any

import requests

PERSPECTIVE_API_KEY_ENV = "PERSPECTIVE_API_KEY"
PERSPECTIVE_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def profile_moderation(text: str) -> dict[str, Any]:
    params = {"key": os.environ.get(PERSPECTIVE_API_KEY_ENV, "")}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}},
        "doNotStore": True,
        "languages": ["en"],
    }
    response = requests.post(PERSPECTIVE_HOST, params=params, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
