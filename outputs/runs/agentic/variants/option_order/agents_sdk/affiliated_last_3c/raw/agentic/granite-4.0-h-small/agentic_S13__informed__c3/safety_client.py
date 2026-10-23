import os
from typing import Dict, Any
import requests

# Provider: Perspective API (REST)
API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

def safety_client(text: str, attributes: list = ["TOXICITY"]) -> Dict[str, Any]:
    """Wrapper client that sends text to Perspective API and returns raw response."""
    payload = {
        "comment": {"text": text, "type": "PLAIN_TEXT"},
        "requestedAttributes": {attr: {} for attr in attributes}
    }
    headers = {
        "content-type": "application/json",
        "x-goog-api-key": PERSPECTIVE_API_KEY
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
