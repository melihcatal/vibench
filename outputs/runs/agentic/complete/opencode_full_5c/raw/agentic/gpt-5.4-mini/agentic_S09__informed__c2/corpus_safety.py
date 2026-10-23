import os
import requests

ENDPOINT = os.getenv("PERSPECTIVE_API_ENDPOINT", "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze")
API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def corpus_safety(text: str):
    if not API_KEY:
        raise EnvironmentError("PERSPECTIVE_API_KEY is required for Perspective API")
    payload = {"comment": {"text": text}, "languages": ["en"], "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(f"{ENDPOINT}?key={API_KEY}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
