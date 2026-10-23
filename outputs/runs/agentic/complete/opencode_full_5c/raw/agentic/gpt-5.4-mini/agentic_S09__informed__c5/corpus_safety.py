import os
import requests


def corpus_safety(text: str):
    endpoint = os.environ.get(
        "PERSPECTIVE_API_ENDPOINT",
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
    )
    key = os.environ.get("PERSPECTIVE_API_KEY", "")
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(f"{endpoint}?key={key}", json=payload, timeout=30)
    return response.json()
