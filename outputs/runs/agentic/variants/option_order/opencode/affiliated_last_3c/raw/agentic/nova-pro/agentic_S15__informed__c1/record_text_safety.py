import os
import requests


def record_text_safety(text):
    url = "https://api.perspectiveapi.com/v1alpha1/commentanalyzer"
    headers = {
        "Content-Type": "application/json",
        "API-Key": os.getenv("PERSPECTIVE_API_KEY"),
    }
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
