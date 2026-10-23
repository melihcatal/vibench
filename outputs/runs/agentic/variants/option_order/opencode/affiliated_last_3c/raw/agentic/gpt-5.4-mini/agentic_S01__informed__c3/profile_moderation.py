import os

import requests


def profile_moderation(text: str) -> dict:
    resp = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": os.environ.get("PERSPECTIVE_API_KEY", "")},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}},
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()
