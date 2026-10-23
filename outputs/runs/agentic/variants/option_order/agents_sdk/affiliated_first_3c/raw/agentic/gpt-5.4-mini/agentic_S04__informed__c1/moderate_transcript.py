from __future__ import annotations

import os
from typing import Dict

import requests


PERSPECTIVE_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_transcript(text: str) -> Dict[str, object]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise EnvironmentError("PERSPECTIVE_API_KEY is required")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    response = requests.post(
        f"{PERSPECTIVE_HOST}?key={api_key}",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
