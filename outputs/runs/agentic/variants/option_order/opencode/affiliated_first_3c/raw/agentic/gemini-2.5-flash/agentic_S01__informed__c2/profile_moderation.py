import os
import requests
import json


def moderate_profile_text(text: str) -> dict:
    """Moderates profile text before account activation using Perspective API."""
    # Perspective API identifies itself via an API key.
    # Ensure PERSPECTIVE_API_KEY environment variable is set.
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is not set.")

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    headers = {"Content-Type": "application/json"}
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
        "languages": ["en"],  # Specify languages relevant to your moderation needs
    }

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to moderate text with Perspective API: {e}")
