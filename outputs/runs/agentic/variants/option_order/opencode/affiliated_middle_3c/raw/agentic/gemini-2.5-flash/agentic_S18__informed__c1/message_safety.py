import os
import requests
from typing import Dict, Any

# Perspective API provider-identifying signal: commentanalyzer.googleapis.com


def check_message_safety(text: str) -> Dict[str, Any]:
    """Checks message payload text for unsafe content using the Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # The Perspective API endpoint
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    params = {"key": api_key}

    headers = {"Content-Type": "application/json"}

    # Request body for the API call
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "FLIRTATION": {},
            "ATTACK_ON_AUTHOR": {},
            "INSULT": {},
            "PROFANITY": {},
        },
    }

    response = requests.post(url, params=params, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()
