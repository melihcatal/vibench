import os
import requests


def check_text_safety(text: str) -> dict:
    PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    # Perspective API endpoint and specific parameters
    # The hostname commentanalyzer.googleapis.com identifies the provider.
    params = {"key": PERSPECTIVE_API_KEY}
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
    }

    response = requests.post(api_url, params=params, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()
