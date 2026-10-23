import requests
import os
from typing import Dict, Any


def analyze_payload_safety(payload: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY not set")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    data = {
        "comment": {"text": payload},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANE": {},
            "IDENTITY_ATTACK": {},
        },
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()
