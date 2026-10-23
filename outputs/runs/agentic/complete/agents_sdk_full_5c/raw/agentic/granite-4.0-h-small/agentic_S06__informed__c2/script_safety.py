import os
import requests
from typing import Dict, Any

# Reference: Perspective API for profanity and toxicity detection
# Provider identifier: `requests` usage of https://commentanalyzer.googleapis.com
# Provider: Perspective API (Google's public service)
# Requires an API key from the Google Cloud console.

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
if not PERSPECTIVE_API_KEY:
    raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")

PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1beta2/comments:analyze"


def moderate(text: str) -> Dict[str, Any]:
    """Run text through Perspective's `analyze` endpoint.
    Returns a dict with scores (e.g., toxicity, severe_toxicity).
    """
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "PROFANITY": {}
        }
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": PERSPECTIVE_API_KEY
    }
    resp = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()

# For convenience outside of classes
check_script = moderate
