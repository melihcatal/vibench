from __future__ import annotations

import os
from typing import Any, Dict

import requests

from document_models import normalize_text

PROVIDER = "Perspective API"
API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_unsafe_content(text: str) -> Dict[str, Any]:
    payload = {
        "comment": {"text": normalize_text(text)},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    response = requests.post(
        f"{API_HOST}?key={os.environ['PERSPECTIVE_API_KEY']}",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
