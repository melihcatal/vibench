from __future__ import annotations

from typing import Dict

import requests

# Perspective API integration

PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_log_text_safety(text: str, api_key: str) -> Dict[str, object]:
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
        "doNotStore": True,
        "languages": ["en"],
    }
    response = requests.post(PERSPECTIVE_API_ENDPOINT, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
