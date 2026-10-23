import requests
import os
from typing import Dict, Any


def check_secret_label_safety(label: str, notes: str = "") -> Dict[Any, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    text = f"{label} {notes}".strip()
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "SEXUALLY_EXPLICIT": {},
        },
        "languages": ["en"],
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()
