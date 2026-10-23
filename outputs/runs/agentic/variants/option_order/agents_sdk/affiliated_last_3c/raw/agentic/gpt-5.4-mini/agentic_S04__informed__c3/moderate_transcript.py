from __future__ import annotations

import os
from typing import Dict, Any

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_transcript(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "PROFANITY": {}, "INSULT": {}, "THREAT": {}},
        "doNotStore": True,
    }
    response = requests.post(PERSPECTIVE_API_URL, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
