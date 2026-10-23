import os
import requests

class SafetyClient:
    def __init__(self, api_key: str = None, api_endpoint: str = None):
        self.api_key = api_key if api_key else os.getenv("TEXT_CONTENT_SAFETY_API_KEY")
        self.api_endpoint = api_endpoint if api_endpoint else os.getenv("TEXT_CONTENT_SAFETY_API_ENDPOINT", "https://api.safety.example.com/v1/moderate")

        if not self.api_key:
            raise ValueError("API Key not provided and TEXT_CONTENT_SAFETY_API_KEY environment variable not set.")
        if not self.api_endpoint:
            raise ValueError("API Endpoint not provided and TEXT_CONTENT_SAFETY_API_ENDPOINT environment variable not set.")

    def moderate_text(self, text: str):
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
        payload = {
            "text": text
        }
        try:
            response = requests.post(self.api_endpoint, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during moderation request: {e}")
            raise