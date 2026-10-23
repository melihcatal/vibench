import os
import requests


def check_content_safety(text: str, api_key: str):
    """
    Checks narration scripts for unsafe content using Perspective API.
    """
    # Perspective API endpoint
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    # API key from environment variable
    # os.environ.get("PERSPECTIVE_API_KEY")

    params = {
        "key": api_key,
    }

    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
        },
        "languages": ["en"],
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, params=params, json=data, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()
