from typing import Dict, List, Optional, Union
import os
import requests


class TisaneClient:
    """Client for Tisane Text Moderation API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TISANE_API_KEY")
        if not self.api_key:
            raise ValueError("TISANE_API_KEY environment variable not set")
        self.base_url = "https://api.tisane.ai/v1/moderate"

    def moderate_text(self, text: str, categories: Optional[List[str]] = None) -> Dict:
        """Moderate a single text input using Tisane API."""
        payload = {"text": text}
        if categories:
            payload["categories"] = categories
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(self.base_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def moderate_batch(
        self, texts: List[str], categories: Optional[List[str]] = None
    ) -> List[Dict]:
        """Moderate a batch of text inputs using Tisane API."""
        payload = {"texts": texts}
        if categories:
            payload["categories"] = categories
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(self.base_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["results"]


class TisaneRedactor:
    """Redacts unsafe spans from text using Tisane API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TISANE_API_KEY")
        if not self.api_key:
            raise ValueError("TISANE_API_KEY environment variable not set")
        self.base_url = "https://api.tisane.ai/v1/redact"

    def redact(self, text: str, categories: Optional[List[str]] = None) -> Dict:
        """Redact unsafe spans from text."""
        payload = {"text": text}
        if categories:
            payload["categories"] = categories
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(self.base_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
