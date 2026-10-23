from typing import List, Dict, Any
import os
import requests


class CorpusSafetyChecker:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.api_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def check_text_safety(self, text: str) -> Dict[str, Any]:
        """
        Checks corpus text for safety using Perspective API.
        """
        params = {"key": self.api_key}
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

        response = requests.post(self.api_url, params=params, json=data)
        response.raise_for_status()
        return response.json()
