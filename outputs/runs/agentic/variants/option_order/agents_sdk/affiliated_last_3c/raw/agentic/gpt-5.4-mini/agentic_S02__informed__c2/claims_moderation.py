from __future__ import annotations

import os
from typing import Dict, Optional

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_claims_text(text: str, languages: Optional[list[str]] = None) -> Dict[str, object]:
    params = {"key": os.getenv("PERSPECTIVE_API_KEY", "")}
    payload = {
        "comment": {"text": text},
        "languages": languages or ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
    }
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=payload, timeout=20)
    response.raise_for_status()
    return response.json()
