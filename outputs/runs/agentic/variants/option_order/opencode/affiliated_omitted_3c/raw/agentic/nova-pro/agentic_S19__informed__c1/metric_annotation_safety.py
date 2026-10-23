import os

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

import requests


def metric_annotation_safety(text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
    }
    headers = {"Content-Type": "application/json", "API_KEY": PERSPECTIVE_API_KEY}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
