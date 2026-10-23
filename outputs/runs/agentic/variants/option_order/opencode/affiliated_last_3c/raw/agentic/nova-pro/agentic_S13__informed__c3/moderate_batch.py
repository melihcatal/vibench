import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_batch(texts):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    data = {
        "comments": [{"text": text} for text in texts],
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {} for _ in texts},
    }
    headers = {"Content-Type": "application/json", "API_KEY": PERSPECTIVE_API_KEY}
    response = requests.post(url, json=data, headers=headers)
    return response.json()
