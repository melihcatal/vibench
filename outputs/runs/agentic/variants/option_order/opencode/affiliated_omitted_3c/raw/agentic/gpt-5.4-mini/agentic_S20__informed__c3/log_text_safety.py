import os

import requests


def log_text_safety(text: str) -> dict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    response = requests.post(
        url,
        params={"key": api_key},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
