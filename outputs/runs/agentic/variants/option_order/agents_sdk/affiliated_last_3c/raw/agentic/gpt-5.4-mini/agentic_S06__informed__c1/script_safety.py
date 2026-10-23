from __future__ import annotations

import os
from typing import Any, Dict

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_script_safety(text: str) -> Dict[str, Any]:
    key = os.getenv("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    response = requests.post(f"{PERSPECTIVE_API_URL}?key={key}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
