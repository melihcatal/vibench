import os

import requests


def check_corpus_text(text: str):
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    params = {"key": api_key}
    return requests.post(url, json=payload, params=params, timeout=30).json()
