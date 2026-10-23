import os

import requests


PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_prompt_safety(text: str, api_key: str | None = None) -> dict:
    key = api_key or os.getenv("PERSPECTIVE_API_KEY")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}}
    }
    response = requests.post(f"{PERSPECTIVE_ENDPOINT}?key={key}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
