import os
import requests


def check_script_safety(text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
