import os
import requests
import json

class SafetyClient:
    def __init__(self):
        self.api_key = os.getenv("CONTENT_SAFETY_API_KEY")
        self.api_endpoint = os.getenv("CONTENT_SAFETY_API_ENDPOINT", "https://api.contentsafety.example.com/v1/moderate")

        if not self.api_key:
            raise ValueError("CONTENT_SAFETY_API_KEY environment variable not set.")

    def moderate_text(self, text: str) -> dict:
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
        payload = {
            "text": text
        }
        try:
            response = requests.post(self.api_endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during API call: {e}")
            raise