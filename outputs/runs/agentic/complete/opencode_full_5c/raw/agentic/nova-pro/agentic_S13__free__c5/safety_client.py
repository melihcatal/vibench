import os
import requests


class SafetyClient:
    def __init__(self):
        self.api_key = os.getenv("SAFETY_API_KEY")
        self.api_url = "https://api.safetyprovider.com/moderate"

    def moderate(self, text: str) -> dict:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"text": text}
        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
