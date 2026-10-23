import requests
import os
from typing import Dict, Any


def check_payload_safety(payload: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    body = {
        "comment": {"text": payload},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "SEXUALLY_EXPLICIT": {},
            "THREAT": {},
        },
        "doNotStore": True,
    }
    resp = requests.post(url, json=body)
    resp.raise_for_status()
    return resp.json()
