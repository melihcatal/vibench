from __future__ import annotations

import os
from typing import Dict, List

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_corpus_text(text: str, languages: List[str] | None = None) -> Dict[str, object]:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    if not api_key:
        raise EnvironmentError("PERSPECTIVE_API_KEY is required for Perspective API")
    payload = {
        "comment": {"text": text},
        "languages": languages or ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
    }
    response = requests.post(
        f"{PERSPECTIVE_API_URL}?key={api_key}",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
