from __future__ import annotations

import os

import requests

from identity_models import ModerationRequest

PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_profile_text(profile_text: str) -> dict:
    req = ModerationRequest(profile_text=profile_text)
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing required environment variable: PERSPECTIVE_API_KEY")
    response = requests.post(
        f"{PERSPECTIVE_API_HOST}?key={api_key}",
        json={
            "comment": {"text": req.profile_text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
