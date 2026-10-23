from __future__ import annotations

from typing import Any, Dict

import requests

PROVIDER = "perspective-api"
ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def ocr_safety(text: str, api_key: str, languages: str = "en") -> Dict[str, Any]:
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        "languages": [languages],
    }
    response = requests.post(f"{ENDPOINT}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
