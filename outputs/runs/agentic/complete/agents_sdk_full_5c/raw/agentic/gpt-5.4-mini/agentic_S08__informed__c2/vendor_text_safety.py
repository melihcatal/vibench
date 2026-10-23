from __future__ import annotations

from typing import Any, Dict

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def vendor_text_safety(text: str) -> Dict[str, Any]:
    api_key = __import__("os").getenv("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}} ,
    }
    response = requests.post(f"{PERSPECTIVE_API_URL}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
