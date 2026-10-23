from __future__ import annotations

import os

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def profile_moderation(text: str, requested_attributes: list[str] | None = None) -> dict:
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in (requested_attributes or ["TOXICITY", "INSULT", "PROFANITY"])},
        "languages": ["en"],
    }
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
