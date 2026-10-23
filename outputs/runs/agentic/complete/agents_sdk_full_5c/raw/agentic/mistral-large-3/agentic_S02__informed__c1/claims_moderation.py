import requests
import os
from typing import Dict


def moderate_claims(text: str) -> Dict:
    perspective_api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={perspective_api_key}"

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}}
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()