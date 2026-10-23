import os
import requests  # PERSPECTIVE-specific


class ClaimsModerator:
    def __init__(self):
        self.api_key = os.environ.get("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable must be set.")
        self.endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"  # PERSPECTIVE-specific

    def moderate_text(self, text: str) -> dict:
        url = f"{self.endpoint}?key={self.api_key}"
        data = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
