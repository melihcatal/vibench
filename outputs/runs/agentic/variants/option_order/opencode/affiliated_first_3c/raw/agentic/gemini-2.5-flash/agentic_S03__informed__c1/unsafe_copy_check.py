import requests
import os
from typing import Dict, Any


def check_unsafe_content(text: str) -> Dict[str, Any]:
    """Checks localized copy for unsafe content using Perspective API."""
    API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
    if not API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={API_KEY}"

    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
    }

    data = {
        "comment": {"text": text},
        "languages": [
            "en"
        ],  # Assuming content is in English for analysis, adjust if needed
        "requestedAttributes": requested_attributes,
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}
