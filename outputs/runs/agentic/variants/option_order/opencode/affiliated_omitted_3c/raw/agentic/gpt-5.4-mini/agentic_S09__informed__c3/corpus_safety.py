import os
import requests


def check_corpus_text(text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
    }
    response = requests.post(url, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()

