from __future__ import annotations

import os
from typing import Any, Dict

import requests

from document_models import OCRResponse


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_document_safety(response: OCRResponse) -> Dict[str, Any]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "").strip()
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    payload = {
        "comment": {"text": response.text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
        "languages": ["en"],
    }
    r = requests.post(f"{PERSPECTIVE_API_URL}?key={api_key}", json=payload, timeout=30)
    r.raise_for_status()
    return r.json()
