import os
import requests


class PerspectiveClient:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.base_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def analyze_text(self, text, attributes, do_not_store=False):
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

        payload = {
            "comment": {"text": text},
            "requestedAttributes": {attr: {} for attr in attributes},
            "doNotStore": do_not_store,
        }
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}

        response = requests.post(
            self.base_url, headers=headers, json=payload, params=params
        )
        response.raise_for_status()
        return response.json()
