"""
Local configuration and client helper utilities for Text Content Safety.
"""
import os
from typing import Dict, List, Optional

from safety_models import SafetyRequest, SafetyResponse, normalize_azure_response


class AzureContentSafetyClient:
    """Client for Azure AI Content Safety."""

    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        if not self.endpoint or not self.key:
            raise ValueError("Azure Content Safety credentials not configured")

    def moderate(self, request: SafetyRequest) -> SafetyResponse:
        """Moderate text using Azure AI Content Safety."""
        import requests
        url = f"{self.endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": request["text"],
            "categories": request.get("categories", ["Hate", "SelfHarm", "Sexual", "Violence"]),
            "outputType": "FourSeverityLevels"
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return normalize_azure_response(response.json(), request["text"])