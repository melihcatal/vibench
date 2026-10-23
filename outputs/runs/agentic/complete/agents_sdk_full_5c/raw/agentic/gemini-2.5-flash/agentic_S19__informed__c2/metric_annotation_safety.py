import requests
import os

PERSPECTIVE_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_annotation_safety(text: str) -> dict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    params = {
        'key': api_key
    }
    data = {
        'comment': { 'text': text },
        'requestedAttributes': { 'TOXICITY': {} }
    }

    response = requests.post(PERSPECTIVE_API_BASE_URL, params=params, json=data)
    response.raise_for_status()
    return response.json()
