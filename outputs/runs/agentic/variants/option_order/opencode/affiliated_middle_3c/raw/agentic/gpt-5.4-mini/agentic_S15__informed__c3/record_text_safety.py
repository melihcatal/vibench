import os

import requests


def check_text_safety(text):
    endpoint = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    params = {"key": os.getenv("PERSPECTIVE_API_KEY", "")}
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(endpoint, params=params, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
