import requests
import os
from typing import Dict, Any


def message_safety(text: str) -> Dict[str, Any]:
    """
    Checks message payload text for unsafe content using Perspective API.

    Args:
        text: Text to analyze for unsafe content.

    Returns:
        Dictionary containing toxicity scores and analysis results.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

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
        "languages": ["en"],
    }

    response = requests.post(url, json=data)
    response.raise_for_status()

    return response.json()
