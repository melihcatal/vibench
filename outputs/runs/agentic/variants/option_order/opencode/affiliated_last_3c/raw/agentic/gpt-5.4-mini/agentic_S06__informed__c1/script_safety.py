import os

import requests


def check_script_safety(text: str) -> dict:
    key = os.environ["PERSPECTIVE_API_KEY"]
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        "doNotStore": True,
        "languages": ["en"],
    }
    response = requests.post(url, params={"key": key}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
