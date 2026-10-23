import os

import requests


PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_corpus_text(text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }
    params = {"key": api_key} if api_key else {}
    response = requests.post(PERSPECTIVE_API_HOST, params=params, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("attributeScores", {}).get("TOXICITY", {})
