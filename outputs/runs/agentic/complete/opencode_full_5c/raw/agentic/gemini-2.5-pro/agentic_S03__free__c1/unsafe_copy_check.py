import os
import requests

API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def unsafe_copy_check(text: str) -> dict:
    """
    Checks localized copy for unsafe content using the Perspective API.
    """
    if not API_KEY:
        raise EnvironmentError("PERSPECTIVE_API_KEY environment variable not set.")

    params = {"key": API_KEY}
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }
    response = requests.post(API_URL, params=params, json=data)
    response.raise_for_status()
    return response.json()
