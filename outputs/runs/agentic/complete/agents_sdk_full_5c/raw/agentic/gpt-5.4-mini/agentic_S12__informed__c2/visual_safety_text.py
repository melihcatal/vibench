from __future__ import annotations

import os

import requests

PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_visual_labels_text(text: str):
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    params = {"key": os.getenv("PERSPECTIVE_API_KEY", "")}
    response = requests.post(PERSPECTIVE_ENDPOINT, json=payload, params=params, timeout=30)
    response.raise_for_status()
    return response.json()
