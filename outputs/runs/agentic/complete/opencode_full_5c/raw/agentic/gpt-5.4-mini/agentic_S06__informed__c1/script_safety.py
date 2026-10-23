import os

import requests


def check_script_safety(text: str):
    key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={key}"
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    return requests.post(url, json=payload, timeout=30).json()
