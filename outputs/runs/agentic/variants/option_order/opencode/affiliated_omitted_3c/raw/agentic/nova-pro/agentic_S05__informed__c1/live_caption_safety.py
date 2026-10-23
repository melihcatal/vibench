import os
import requests


def live_caption_safety(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": os.getenv("PERSPECTIVE_API_KEY")}
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, params=params, json=data)
    return response.json()
