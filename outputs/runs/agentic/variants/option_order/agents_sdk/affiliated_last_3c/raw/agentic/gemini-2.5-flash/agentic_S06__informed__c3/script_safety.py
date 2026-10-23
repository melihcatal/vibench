
import os
import requests

def check_script_safety(text: str) -> dict:
    """Checks narration scripts for unsafe content using Perspective API.

    Args:
        text: The script content to check.

    Returns:
        A dictionary containing the safety assessment from Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=" + api_key

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status() # Raise an exception for HTTP errors

    return response.json()
