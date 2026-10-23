# Placeholder – check safety of extracted text using Perspective API
from typing import Dict
import json
import requests

# Perspective API configuration (service=Perspective API; sdk=requests; interface=rest; auth=PERSPECTIVE_API_KEY)
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def check_safety(text: str) -> Dict:
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
        },
    }
    headers = {
        "X-Goog-Api-Key": PERSPECTIVE_API_KEY,
        "Content-Type": "application/json",
    }
    response = requests.post(PERSPECTIVE_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
