import os

import requests


def payload_safety(text):
    endpoint = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(
        endpoint,
        params={"key": os.getenv("PERSPECTIVE_API_KEY", "")},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
