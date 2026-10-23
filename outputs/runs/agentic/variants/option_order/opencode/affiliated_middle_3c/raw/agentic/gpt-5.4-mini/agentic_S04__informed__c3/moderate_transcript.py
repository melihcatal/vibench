import os

import requests


def moderate_transcript(text: str):
    key = os.environ.get("PERSPECTIVE_API_KEY", "")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    response = requests.post(
        url,
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        params={"key": key},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
