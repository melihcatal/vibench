import os

import requests


def check_script_safety(text: str) -> dict:
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": os.environ["PERSPECTIVE_API_KEY"]}
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    return requests.post(url, params=params, json=payload, timeout=30).json()
