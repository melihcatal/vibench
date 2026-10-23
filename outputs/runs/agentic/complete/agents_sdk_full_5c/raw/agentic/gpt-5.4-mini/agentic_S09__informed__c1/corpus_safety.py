from __future__ import annotations

import os
from typing import Any

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_corpus_text(text: str) -> dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required for Perspective API safety checks.")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
        "doNotStore": True,
        "languages": ["en"],
    }
    response = requests.post(PERSPECTIVE_API_URL, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
