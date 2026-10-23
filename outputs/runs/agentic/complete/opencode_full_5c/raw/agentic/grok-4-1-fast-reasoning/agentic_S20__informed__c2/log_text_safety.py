import requests
import os
from typing import Dict, Any

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def check_log_safety(text: str) -> Dict[str, Any]:
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
            "PROFANITY": {},
            "SEXUALLY_EXPLICIT": {},
        },
        "doNotStore": True,
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
