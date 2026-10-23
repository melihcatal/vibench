import os
import requests


class PerspectiveAPIClient:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")
        self.base_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def analyze_text(self, text: str) -> dict:
        url = f"{self.base_url}?key={self.api_key}"
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
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()


def check_safety(text: str) -> dict:
    client = PerspectiveAPIClient()
    return client.analyze_text(text)
