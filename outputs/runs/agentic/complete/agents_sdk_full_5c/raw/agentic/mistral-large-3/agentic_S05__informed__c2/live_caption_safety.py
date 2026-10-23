import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_unsafe_content(text: str, threshold: float = 0.7) -> bool:
    if not text.strip():
        return False
    params = {
        "key": PERSPECTIVE_API_KEY
    }
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {}
        },
        "languages": ["en"]
    }
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=data)
    response.raise_for_status()
    attributes = response.json().get("attributeScores", {})
    for attribute in attributes.values():
        if attribute["summaryScore"]["value"] > threshold:
            return True
    return False