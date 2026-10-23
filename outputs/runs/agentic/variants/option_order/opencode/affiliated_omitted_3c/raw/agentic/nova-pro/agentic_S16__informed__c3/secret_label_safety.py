import requests
import os


def secret_label_safety(api_key, text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
        "key": api_key,
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
