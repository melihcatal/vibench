from typing import Dict, Any
import os
import requests


class AzureContentSafetyChecker:
    """Check narration scripts for unsafe content using Azure AI Content Safety."""

    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        self.headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json",
        }

    def check_safety(self, text: str) -> Dict[str, Any]:
        """Check text for unsafe content."""
        url = f"{self.endpoint}/contentsafety/text:analyze"
        body = {
            "text": text,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "outputType": "FourSeverityLevels",
        }
        response = requests.post(url, headers=self.headers, json=body)
        response.raise_for_status()
        return response.json()
