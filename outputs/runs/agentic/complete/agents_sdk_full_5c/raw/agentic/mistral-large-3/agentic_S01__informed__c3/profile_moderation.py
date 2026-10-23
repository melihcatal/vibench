import os
import requests
from typing import Dict, Any


class ProfileModerator:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def moderate_profile_text(self, text: str) -> Dict[str, Any]:
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
            "doNotStore": True,
        }
        params = {"key": self.api_key}
        response = requests.post(self.url, params=params, json=payload)
        response.raise_for_status()
        return response.json()}