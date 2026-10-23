from __future__ import annotations

from typing import Any, Dict

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def vendor_text_safety(text: str, api_key: str) -> Dict[str, Any]:
    params = {"key": api_key}
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
