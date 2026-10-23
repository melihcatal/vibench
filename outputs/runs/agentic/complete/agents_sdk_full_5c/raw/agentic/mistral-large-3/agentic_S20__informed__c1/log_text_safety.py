import os
import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def check_log_text_safety(text: str) -> dict:
    """Check log message text for unsafe content using Perspective API."""
    params = {"key": PERSPECTIVE_API_KEY}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {}
        }
    }
    
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=payload)
    response.raise_for_status()
    
    return response.json()