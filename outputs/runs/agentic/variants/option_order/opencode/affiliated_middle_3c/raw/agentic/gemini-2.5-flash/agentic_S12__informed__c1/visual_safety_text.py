import os
import requests
from typing import Dict, Any


def check_visual_labels_for_unsafe_text(text_content: str) -> Dict[str, Any]:
    """
    Checks generated visual labels for unsafe text using the Perspective API.
    The PERSPECTIVE_API_KEY environment variable must be set.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    data = {
        "comment": {"text": text_content},
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
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()
