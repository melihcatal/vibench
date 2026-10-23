from __future__ import annotations

from typing import Any, Dict

import requests

from database_models import NormalizedResponse

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_text_safety(text: str, attributes: Dict[str, Any] | None = None) -> NormalizedResponse:
    params = {"key": __import__("os").environ["PERSPECTIVE_API_KEY"]}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": attributes or {"TOXICITY": {}},
        "languages": ["en"],
    }
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=payload, timeout=30)
    response.raise_for_status()
    return NormalizedResponse(ok=True, data=response.json())
