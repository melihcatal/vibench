import os
import requests
from typing import Dict, Any

PERSPECTIVE_API_KEY = os.environ["PERSPECTIVE_API_KEY"]

def record_text_safety(text: str) -> Dict[str, Any]:
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()