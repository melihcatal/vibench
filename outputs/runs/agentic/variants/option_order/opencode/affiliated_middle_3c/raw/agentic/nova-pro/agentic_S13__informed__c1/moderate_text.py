import os
import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_text(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('PERSPECTIVE_API_KEY')}",
    }
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(PERSPECTIVE_API_URL, headers=headers, json=data)
    return response.json()
