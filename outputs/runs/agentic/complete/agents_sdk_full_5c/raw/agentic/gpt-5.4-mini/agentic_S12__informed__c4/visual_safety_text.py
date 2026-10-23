import os

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_visual_safety_text(text: str) -> dict:
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
    }
    params = {"key": os.environ.get("PERSPECTIVE_API_KEY", "")}
    response = requests.post(PERSPECTIVE_API_URL, json=payload, params=params, timeout=30)
    response.raise_for_status()
    return response.json()
