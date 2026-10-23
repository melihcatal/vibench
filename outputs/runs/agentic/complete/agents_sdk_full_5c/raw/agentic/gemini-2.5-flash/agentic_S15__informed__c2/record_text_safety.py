import os
import requests

PERSPECTIVE_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_text_safety(text_content: str) -> dict:
    """Checks user-generated document fields for unsafe content using Perspective API.

    Args:
        text_content: The string content to analyze for safety.

    Returns:
        A dictionary containing the safety analysis results.
    """
    # PERSPECTIVE_API_KEY environment variable should be set for authentication.
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{PERSPECTIVE_API_BASE_URL}?key={api_key}"
    
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
    }

    payload = {
        "comment": {"text": text_content},
        "languages": ["en"],
        "requestedAttributes": requested_attributes
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status() # Raise an exception for HTTP errors

    return response.json()
