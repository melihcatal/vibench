import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_batch(texts):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    data = {
        "comments": [{"text": text} for text in texts],
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
