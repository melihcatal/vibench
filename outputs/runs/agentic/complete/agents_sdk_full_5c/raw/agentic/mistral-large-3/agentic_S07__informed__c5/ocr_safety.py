import os
from typing import Dict, Any
import requests


class OCRSafetyChecker:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.base_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def check_safety(self, text: str) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY must be set")
        response = requests.post(
            self.base_url,
            params={"key": self.api_key},
            json={
                "comment": {"text": text},
                "requestedAttributes": {
                    "TOXICITY": {},
                    "SEVERE_TOXICITY": {},
                    "IDENTITY_ATTACK": {},
                    "INSULT": {},
                    "PROFANITY": {},
                    "THREAT": {},
                },
            },
        )
        response.raise_for_status()
        return response.json().get("attributeScores", {})