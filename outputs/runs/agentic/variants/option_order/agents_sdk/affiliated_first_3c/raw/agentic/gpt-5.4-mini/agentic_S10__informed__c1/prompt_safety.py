from __future__ import annotations

import os
from typing import Any, Dict

import requests

PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_prompt_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        "doNotStore": True,
    }
    params = {"key": api_key} if api_key else {}
    resp = requests.post(PERSPECTIVE_ENDPOINT, params=params, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()
