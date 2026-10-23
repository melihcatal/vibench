from __future__ import annotations

import requests


def profile_moderation(text: str) -> dict:
    resp = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        params={"key": __import__("os").getenv("PERSPECTIVE_API_KEY", "")},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()
