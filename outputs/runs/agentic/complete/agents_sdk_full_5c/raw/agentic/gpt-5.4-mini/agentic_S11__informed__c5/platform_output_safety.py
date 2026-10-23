from __future__ import annotations

import os
from typing import Any, Dict

import requests


PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_platform_output_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(
        f"{PERSPECTIVE_URL}?key={api_key}",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
