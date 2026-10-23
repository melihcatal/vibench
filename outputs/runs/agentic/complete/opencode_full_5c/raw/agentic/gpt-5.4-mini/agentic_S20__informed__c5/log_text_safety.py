import os
import requests


def is_safe(text: str) -> dict:
    endpoint = os.getenv("PERSPECTIVE_API_ENDPOINT", "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze")
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
        "languages": ["en"],
    }
    response = requests.post(endpoint, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
