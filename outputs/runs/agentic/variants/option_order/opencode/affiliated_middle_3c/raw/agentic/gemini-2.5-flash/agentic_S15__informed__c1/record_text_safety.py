import os
import requests


def check_text_safety(text_content: str) -> dict:
    """Checks user-generated document fields for unsafe content using Perspective API.

    Args:
        text_content (str): The text content to check for safety.

    Returns:
        dict: A dictionary containing the safety analysis results.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # Perspective API expects a specific request format
    request_body = {
        "comment": {"text": text_content},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],  # Specify language if known
    }

    response = requests.post(url, json=request_body)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()
