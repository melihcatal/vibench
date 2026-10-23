from typing import Dict, Any
import requests
import os

# Provider-specific: OpenAI Moderation API
# API Endpoint: https://api.openai.com/v1/moderations
# Environment variable: OPENAI_API_KEY


class MessageSafetyChecker:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_url = "https://api.openai.com/v1/moderations"

    def check_safety(self, text: str) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"input": text}
        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
