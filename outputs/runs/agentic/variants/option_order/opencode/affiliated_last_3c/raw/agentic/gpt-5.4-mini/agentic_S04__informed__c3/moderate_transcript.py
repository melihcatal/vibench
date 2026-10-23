import os

import requests


def moderate_transcript(text: str):
    key = os.getenv("PERSPECTIVE_API_KEY")
    if not key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={key}"
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()
