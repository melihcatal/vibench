import os
import requests


def moderate_transcript(text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required.")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANE": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }
    response = requests.post(url, params={"key": api_key}, json=payload)
    response.raise_for_status()
    return response.json()
