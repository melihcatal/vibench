from __future__ import annotations

import os

import requests


def check_script_safety(text: str) -> dict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required for Perspective API")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    response = requests.post(url, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
