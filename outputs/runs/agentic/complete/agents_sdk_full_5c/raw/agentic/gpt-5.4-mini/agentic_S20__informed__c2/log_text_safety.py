from __future__ import annotations

import os
from typing import Any, Dict

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def log_text_safety(text: str) -> Dict[str, Any]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
        "doNotStore": True,
    }
    response = requests.post(
        f"{PERSPECTIVE_API_URL}?key={api_key}",
        json=payload,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
