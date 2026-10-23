import os
import requests

PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def message_safety(text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(f"{PERSPECTIVE_URL}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
