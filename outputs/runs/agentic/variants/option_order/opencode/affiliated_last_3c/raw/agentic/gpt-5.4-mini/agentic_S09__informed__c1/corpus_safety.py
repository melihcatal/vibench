import os

import requests


def corpus_safety(text: str):
    endpoint = os.getenv(
        "PERSPECTIVE_API_ENDPOINT",
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
    )
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
    }
    response = requests.post(f"{endpoint}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data
