from __future__ import annotations

import os
from typing import Iterable

import requests

PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY_ENV = "PERSPECTIVE_API_KEY"


def check_payload_safety(text: str, attributes: Iterable[str] = ("TOXICITY", "SEVERE_TOXICITY")) -> dict:
    api_key = os.environ.get(PERSPECTIVE_API_KEY_ENV, "")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "doNotStore": True,
    }
    resp = requests.post(f"{PERSPECTIVE_API_HOST}?key={api_key}", json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()
