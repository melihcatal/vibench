import os
import requests


class VendorTextSafety:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.api_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def moderate(self, text: str) -> Dict[str, Any]:
        params = {"key": self.api_key}
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
            },
            "languages": ["en"],
        }

        response = requests.post(self.api_url, params=params, json=payload)
        response.raise_for_status()
        return response.json()
