from __future__ import annotations

from typing import Any, Dict, Iterable, List

import requests

PROVIDER_NAME = "Perspective API"
API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_text_safety(text_fields: Dict[str, str], api_key: str | None = None) -> Dict[str, Any]:
    payload = {"comment": {"text": "\n".join(text_fields.values())}, "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}}}
    params = {"key": api_key} if api_key else None
    response = requests.post(API_HOST, json=payload, params=params, timeout=30)
    response.raise_for_status()
    return response.json()
