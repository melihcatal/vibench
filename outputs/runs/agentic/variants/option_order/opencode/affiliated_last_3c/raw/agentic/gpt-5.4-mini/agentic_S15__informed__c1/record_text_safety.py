import os

import requests


def record_text_safety(text):
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
