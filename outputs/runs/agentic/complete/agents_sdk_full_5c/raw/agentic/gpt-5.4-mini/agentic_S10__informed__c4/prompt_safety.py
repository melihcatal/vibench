from __future__ import annotations

import os
from typing import Dict

import requests

PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_prompt_safety(text: str) -> Dict[str, object]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    params = {"key": api_key} if api_key else {}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}, "PROFANITY": {}},
        "languages": ["en"],
    }
    response = requests.post(PERSPECTIVE_ENDPOINT, params=params, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data
