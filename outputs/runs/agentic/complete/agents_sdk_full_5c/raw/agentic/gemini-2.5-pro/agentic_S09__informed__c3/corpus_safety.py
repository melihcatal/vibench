import os
import requests
import json

def check_text_safety_perspective(text: str) -> dict:
    """
    Checks text for toxicity using the Google Perspective API.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary containing the toxicity analysis from the API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }

    response = requests.post(url, data=json.dumps(payload))
    response.raise_for_status()

    return response.json()

