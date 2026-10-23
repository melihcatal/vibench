import os
import requests
from typing import Dict, Any

PERSPECTIVE_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1"


def moderate_transcript_text(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"{PERSPECTIVE_API_BASE_URL}/comments:analyze?key={api_key}"

    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
