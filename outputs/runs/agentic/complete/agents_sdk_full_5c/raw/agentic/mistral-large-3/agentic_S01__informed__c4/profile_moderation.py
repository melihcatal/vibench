import os
import requests
from typing import Dict, Any

class ProfileModerator:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={self.api_key}"

    def moderate_text(self, text: str) -> Dict[str, Any]:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {}
            },
            "languages": ["en"]
        }
        response = requests.post(self.url, json=payload)
        response.raise_for_status()
        return response.json()