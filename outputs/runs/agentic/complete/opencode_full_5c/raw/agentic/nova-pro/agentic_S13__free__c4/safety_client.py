import os
import requests


class SafetyClient:
    def __init__(self):
        self.api_key = os.getenv("SAFETY_API_KEY")
        self.api_url = "https://api.safetyprovider.com/moderate"

    def moderate_text(self, text):
        response = requests.post(
            self.api_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"text": text},
        )
        return response.json()

    def redact_unsafe(self, text):
        response = requests.post(
            self.api_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"text": text, "action": "redact"},
        )
        return response.json()

    def apply_thresholds(self, text, thresholds):
        response = requests.post(
            self.api_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"text": text, "thresholds": thresholds},
        )
        return response.json()
