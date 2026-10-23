import os
import requests
from typing import Dict, Any

def check_message_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}}
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
