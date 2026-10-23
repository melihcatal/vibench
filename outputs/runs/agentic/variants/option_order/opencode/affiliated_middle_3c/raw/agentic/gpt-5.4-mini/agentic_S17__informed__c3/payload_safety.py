import os

import requests


def payload_safety(text: str):
    endpoint = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    headers = {
        "X-Goog-Api-Key": os.getenv("PERSPECTIVE_API_KEY", ""),
        "Content-Type": "application/json",
    }
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    return requests.post(endpoint, json=payload, headers=headers, timeout=30).json()
