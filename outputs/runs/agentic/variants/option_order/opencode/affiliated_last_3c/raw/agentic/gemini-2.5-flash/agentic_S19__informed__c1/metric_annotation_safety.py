import os
import requests


def check_annotation_safety(text):
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": api_key}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, params=params, json=data, headers=headers)
    response.raise_for_status()
    return response.json()
