import os
import requests
from typing import Dict


def moderate_transcript(text: str) -> Dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required.")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "IDENTITY_ATTACK": {},
        },
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()
