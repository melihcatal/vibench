import os
import requests


def check_script_safety(text: str, api_key: str) -> dict:
    """
    Checks narration scripts for unsafe content using Perspective API.
    Requires PERSPECTIVE_API_KEY to be set.
    """
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
