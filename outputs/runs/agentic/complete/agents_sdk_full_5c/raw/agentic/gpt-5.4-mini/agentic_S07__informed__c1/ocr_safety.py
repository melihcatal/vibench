from __future__ import annotations

import os
from typing import Dict

import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY", "")
PERSPECTIVE_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_document_text(text: str) -> Dict[str, object]:
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
        "languages": ["en"],
    }
    response = requests.post(f"{PERSPECTIVE_HOST}?key={PERSPECTIVE_API_KEY}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
