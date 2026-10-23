from __future__ import annotations

import os
from typing import Any, Dict

import requests

PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY", "")


def check_prompt_safety(text: str) -> Dict[str, Any]:
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    response = requests.get(PERSPECTIVE_ENDPOINT, params={"key": PERSPECTIVE_API_KEY}, json=payload, timeout=20)
    response.raise_for_status()
    return response.json()
