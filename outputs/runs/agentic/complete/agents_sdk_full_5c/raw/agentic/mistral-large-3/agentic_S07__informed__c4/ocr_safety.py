import os
import requests
from typing import Dict, Any


class ContentSafetyChecker:
    def __init__(self):
        self.api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        if not self.api_key or not self.endpoint:
            raise ValueError(
                "Azure Content Safety endpoint and key must be set as environment variables."
            )

    def check_safety(self, text: str) -> Dict[str, Any]:
        url = f"{self.endpoint}/contentsafety/text:analyze"
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "blocklistNames": [],
            "haltOnBlocklistHit": False,
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()