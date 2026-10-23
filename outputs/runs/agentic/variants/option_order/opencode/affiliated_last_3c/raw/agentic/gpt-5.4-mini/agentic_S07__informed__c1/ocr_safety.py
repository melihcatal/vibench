import os

import requests


def check_safety(text: str):
    response = requests.post(
        os.environ.get(
            "PERSPECTIVE_API_ENDPOINT",
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        ),
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
