import requests
from typing import Dict, Any

class AnnotationSafetyChecker:
    def __init__(self):
        self.api_key = ""  # Uses PERSPECTIVE_API_KEY from environment
        self.api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def check_unsafe_text(self, text: str) -> Dict[str, Any]:
        params = {"key": self.api_key}
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {}
            },
            "languages": ["en"]
        }

        response = requests.post(self.api_url, params=params, json=payload)
        response.raise_for_status()
        return response.json()