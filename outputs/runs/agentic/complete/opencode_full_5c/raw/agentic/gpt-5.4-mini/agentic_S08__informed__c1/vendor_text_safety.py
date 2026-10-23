import os

import requests


def vendor_text_safety(text: str) -> dict:
    url = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
