import os

import requests


def metric_annotation_safety(text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    params = {"key": api_key} if api_key else {}
    response = requests.post(url, params=params, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
