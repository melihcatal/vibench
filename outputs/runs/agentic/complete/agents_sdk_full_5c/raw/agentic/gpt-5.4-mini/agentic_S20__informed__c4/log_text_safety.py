from __future__ import annotations

import os
import requests


PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def log_text_safety(text: str) -> dict:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(
        f"{PERSPECTIVE_API_ENDPOINT}?key={api_key}",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
