import requests
import os


def check_safety_perspective_api(text: str, api_key: str):
    # Perspective API endpoint
    # Provider-identifying signal: commentanalyzer.googleapis.com
    url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + api_key
    )
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
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()
