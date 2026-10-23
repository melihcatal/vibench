import os
import requests
from security_client import get_perspective_api_key

# Google Perspective API endpoint
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_secret_label_safety(text: str) -> dict:
    """Checks secret labels and notes for unsafe text using Perspective API.

    Args:
        text: The text (secret label or note) to check for safety.

    Returns:
        A dictionary containing the Perspective API analysis results.
    """
    api_key = get_perspective_api_key()
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    params = {"key": api_key}

    try:
        response = requests.post(PERSPECTIVE_API_URL, params=params, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error calling Perspective API: {e}")
