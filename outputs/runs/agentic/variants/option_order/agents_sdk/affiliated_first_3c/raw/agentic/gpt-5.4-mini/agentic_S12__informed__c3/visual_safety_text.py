from __future__ import annotations

import os

import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY", "")
PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_generated_visual_labels(labels):
    text = ", ".join(labels)
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(PERSPECTIVE_ENDPOINT, params={"key": PERSPECTIVE_API_KEY}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
