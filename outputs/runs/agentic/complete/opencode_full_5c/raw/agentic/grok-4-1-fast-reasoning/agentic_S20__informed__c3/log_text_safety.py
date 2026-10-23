import os
import requests
from typing import Dict, Any

PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def log_text_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "THREAT": {},
            "PROFANITY": {},
            "SEXUALLY_EXPLICIT": {},
        },
        "languages": ["en"],
    }
    params = {"key": api_key}
    response = requests.post(PERSPECTIVE_URL, json=payload, params=params)
    response.raise_for_status()
    return response.json()
