import os
import requests


def check_secret_label_safety(labels: str, notes: str = "") -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY not set")
    text = f"Secret labels: {labels}. Notes: {notes}"
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": api_key}
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANE": {},
            "IDENTITY_ATTACK": {},
        },
    }
    response = requests.post(url, params=params, json=payload)
    response.raise_for_status()
    return response.json()
