import os
import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def prompt_safety(text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
        "doNotStore": True,
    }
    response = requests.post(
        f"{PERSPECTIVE_API_URL}?key={api_key}",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
