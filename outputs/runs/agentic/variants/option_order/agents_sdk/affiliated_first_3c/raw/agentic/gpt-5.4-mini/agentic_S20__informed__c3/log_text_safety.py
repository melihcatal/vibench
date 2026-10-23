from __future__ import annotations

import os

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def log_text_safety(text: str, languages: list[str] | None = None) -> dict:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
    }
    if languages:
        payload["languages"] = languages
    response = requests.post(PERSPECTIVE_API_URL, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
