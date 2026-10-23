import os
import requests


def record_text_safety(record):
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    response = requests.post(
        url,
        params={"key": api_key},
        json={"comment": {"text": str(record)}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
