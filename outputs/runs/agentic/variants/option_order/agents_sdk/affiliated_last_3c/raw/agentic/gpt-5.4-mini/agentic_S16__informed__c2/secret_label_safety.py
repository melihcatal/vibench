from __future__ import annotations

import os

import requests

# Perspective API integration
API_KEY = os.getenv("PERSPECTIVE_API_KEY", "")
HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def main(text: str) -> dict:
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }
    response = requests.post(f"{HOST}?key={API_KEY}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
