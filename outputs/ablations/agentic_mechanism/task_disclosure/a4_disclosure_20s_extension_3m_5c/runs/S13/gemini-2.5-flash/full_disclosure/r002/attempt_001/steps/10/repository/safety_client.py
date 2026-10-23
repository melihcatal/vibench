
import os
import requests
import json

class TextSafetyClient:
    def __init__(self, api_key=None, api_endpoint=None):
        self.api_key = api_key or os.getenv("TEXT_SAFETY_API_KEY")
        self.api_endpoint = api_endpoint or os.getenv("TEXT_SAFETY_API_ENDPOINT", "https://api.textsafety.example.com/v1/moderate")

        if not self.api_key:
            raise ValueError("API Key not provided and TEXT_SAFETY_API_KEY environment variable not set.")
        if not self.api_endpoint:
            raise ValueError("API Endpoint not provided and TEXT_SAFETY_API_ENDPOINT environment variable not set.")

    def moderate_text(self, text: str):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "text": text
        }
        try:
            response = requests.post(self.api_endpoint, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during text moderation: {e}")
            return {"error": str(e)}

    def batch_moderate_text(self, texts: list[str]):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "texts": texts
        }
        try:
            response = requests.post(f"{self.api_endpoint}/batch", headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during batch text moderation: {e}")
            return {"error": str(e)}
