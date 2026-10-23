from __future__ import annotations

import os
from typing import Any, Dict

import requests


PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_script_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    params = {"key": api_key}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}, "PROFANITY": {}}
    }
    response = requests.post(PERSPECTIVE_ENDPOINT, params=params, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
