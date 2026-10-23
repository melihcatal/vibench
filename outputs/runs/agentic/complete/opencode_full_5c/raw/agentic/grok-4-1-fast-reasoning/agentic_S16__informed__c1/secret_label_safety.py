import os
import requests


def secret_label_safety(text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    data = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
        "languages": ["en"],
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()["attributeScores"]
