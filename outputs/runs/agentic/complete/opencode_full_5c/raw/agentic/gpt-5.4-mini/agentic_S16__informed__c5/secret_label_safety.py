import os

import requests


def secret_label_safety(text: str) -> dict:
    endpoint = os.getenv(
        "PERSPECTIVE_ENDPOINT",
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
    )
    params = {"key": os.getenv("PERSPECTIVE_API_KEY")}
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(endpoint, params=params, json=payload, timeout=30)
    return response.json()
