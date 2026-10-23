import os
import requests
from typing import Dict, Any

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_claims(text: str) -> Dict[str, Any]:
    params = {"key": PERSPECTIVE_API_KEY}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=payload)
    response.raise_for_status()
    return response.json()