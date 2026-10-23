# safety_client.py
import os
import json
import requests
from typing import Any, Dict, List

# Azure AI Content Safety endpoint and key (requires environment variables)
AZURE_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "https://<your-resource>.cognitiveservices.azure.com/content-safety/v1.0/sexual")
AZURE_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

if not AZURE_ENDPOINT or not AZURE_KEY:
    raise RuntimeError("Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables")

HEADERS = {
    "Ocp-Apim-Subscription-Key": AZURE_KEY,
    "Content-Type": "application/json"
}

class TextSafetyClient:
    """Simple client wrapper for Azure AI Content Safety.",
    "The service returns a JSON with a 'results' list, each entry containing category, score, and optional spans.
    """
    def __init__(self):
        self.base_url = AZURE_ENDPOINT
        self.session = requests.Session()

    def analyze_content(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Calls the service for single-document analysis."""
        response = self.session.post(
            f"{self.base_url}/analyze",
            headers=HEADERS,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def analyze_content_batch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Calls the service for batch analysis (up to 256 items)."""
        response = self.session.post(
            f"{self.base_url}/analyzeBatch",
            headers=HEADERS,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    # Simple test when running the file directly
    client = TextSafetyClient()
    test_payload = {
        "content": "This is a test message.",
        "categories": ["hate", "self_harm", "sexual", "violence"]
    }
    print(client.analyze_content(test_payload))