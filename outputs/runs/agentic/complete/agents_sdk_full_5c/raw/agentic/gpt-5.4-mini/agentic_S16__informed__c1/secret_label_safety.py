from __future__ import annotations

import os

import requests


PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def secret_label_safety(text: str) -> dict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
    }
    response = requests.post(f"{PERSPECTIVE_ENDPOINT}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
