import os

import requests


def moderate_vendor_text(text: str) -> dict:
    key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, params={"key": key}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
