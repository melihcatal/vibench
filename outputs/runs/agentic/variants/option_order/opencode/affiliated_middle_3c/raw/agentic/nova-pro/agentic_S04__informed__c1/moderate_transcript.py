import os
import requests


def moderate_transcript(transcript):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    data = {
        "comment": {"text": transcript},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
    }
    headers = {"Content-Type": "application/json", "key": api_key}
    response = requests.post(url, json=data, headers=headers)
    return response.json()
