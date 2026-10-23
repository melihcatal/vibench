from __future__ import annotations

import os

import requests

from identity_models import ModerationRequest


PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def profile_moderation(text: str, locale: str = "en"):
    req = ModerationRequest(text=text, locale=locale).normalized()
    resp = requests.post(
        PERSPECTIVE_ENDPOINT,
        params={"key": os.getenv("PERSPECTIVE_API_KEY", "")},
        json={
            "comment": {"text": req.text},
            "languages": [req.locale],
            "requestedAttributes": {"TOXICITY": {}, "PROFANITY": {}},
        },
        timeout=30,
    )
    resp.raise_for_status()
    return {"provider": "Perspective API", "result": resp.json()}
