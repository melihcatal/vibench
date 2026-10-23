from typing import Dict, Any
import requests
import os

# Provider: Google Cloud Natural Language API
# Model/Service: content moderation (v1)
# API Endpoint: https://language.googleapis.com/v1/documents:moderateText
# Environment Variable: GOOGLE_APPLICATION_CREDENTIALS


class MessageSafetyChecker:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        self.endpoint = "https://language.googleapis.com/v1/documents:moderateText"

    def check_safety(self, text: str) -> Dict[str, Any]:
        """
        Checks message payload text for unsafe content using Google Cloud Natural Language API.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        payload = {"document": {"type": "PLAIN_TEXT", "content": text}}
        response = requests.post(self.endpoint, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
