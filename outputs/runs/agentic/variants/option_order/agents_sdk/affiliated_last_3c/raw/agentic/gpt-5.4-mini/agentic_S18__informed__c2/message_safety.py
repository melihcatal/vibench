from __future__ import annotations

import os

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_message_safety(text: str) -> dict:
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.environ.get("PERSPECTIVE_API_KEY", "")},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
