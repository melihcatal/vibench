from __future__ import annotations

import os

import requests

PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_claims_text(text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "PROFANITY": {}},
    }
    resp = requests.post(f"{PERSPECTIVE_ENDPOINT}?key={api_key}", json=payload, timeout=20)
    resp.raise_for_status()
    return resp.json()
