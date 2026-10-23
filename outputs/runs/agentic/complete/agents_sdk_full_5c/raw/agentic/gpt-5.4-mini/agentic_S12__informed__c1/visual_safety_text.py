from __future__ import annotations

import os

import requests

PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_visual_safety_text(text: str) -> dict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
    params = {"key": api_key}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(PERSPECTIVE_ENDPOINT, params=params, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
