from __future__ import annotations

import os
from typing import Any

import requests

PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def corpus_safety(text: str, attributes: list[str] | None = None) -> dict[str, Any]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise EnvironmentError("PERSPECTIVE_API_KEY is required for Perspective API")
    attrs = attributes or ["TOXICITY", "INSULT", "THREAT"]
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {name: {} for name in attrs},
        "doNotStore": True,
    }
    response = requests.post(
        PERSPECTIVE_API_ENDPOINT,
        params={"key": api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
