import os

import requests


def check_safety(text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
