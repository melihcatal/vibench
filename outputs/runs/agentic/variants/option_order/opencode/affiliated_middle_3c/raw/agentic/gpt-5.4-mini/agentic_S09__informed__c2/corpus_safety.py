import os

import requests


def main(texts: list[str]) -> dict:
    endpoint = os.environ.get(
        "PERSPECTIVE_API_ENDPOINT",
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
    )
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": "\n".join(texts)},
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(
        endpoint, params={"key": api_key}, json=payload, timeout=30
    )
    return response.json()
