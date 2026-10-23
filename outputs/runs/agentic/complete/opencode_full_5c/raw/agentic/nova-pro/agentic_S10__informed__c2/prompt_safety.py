import os
import requests


def check_safety(text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": api_key}
    data = {"comment": {"text": text}, "languages": ["en"]}
    response = requests.post(url, params=params, json=data)
    response.raise_for_status()
    return response.json()
