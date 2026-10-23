import requests
import os
import json
from typing import Dict

def check_payload_safety(text: str) -> Dict:
    """
    Checks decrypted text for unsafe content using Perspective API.
    """
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "doNotStore": True
    }
    response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    return response.json()
