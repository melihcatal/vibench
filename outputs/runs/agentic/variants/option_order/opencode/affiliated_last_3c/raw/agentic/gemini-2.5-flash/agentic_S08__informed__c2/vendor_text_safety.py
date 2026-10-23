import os
import requests
from typing import Dict, Any


def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    # Using the AnalyzeComment endpoint
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
    }

    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": requested_attributes,
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()
