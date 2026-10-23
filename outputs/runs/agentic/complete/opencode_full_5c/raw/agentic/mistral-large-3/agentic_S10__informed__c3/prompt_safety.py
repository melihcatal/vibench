import os
import requests
from typing import Dict, Any


class PromptSafetyChecker:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.base_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def check_safety(self, text: str) -> Dict[str, Any]:
        params = {"key": self.api_key}
        payload = {
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
        response = requests.post(self.base_url, params=params, json=payload)
        response.raise_for_status()
        return response.json()
