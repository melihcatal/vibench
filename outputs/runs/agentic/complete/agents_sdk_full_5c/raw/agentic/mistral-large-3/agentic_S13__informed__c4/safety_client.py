"""
Local configuration and client helper utilities for Azure AI Content Safety.
"""
import os
from typing import Optional
import requests
from safety_models import TextModerationRequest, TextModerationResponse, normalize_azure_scores


class AzureContentSafetyClient:
    """Client for Azure AI Content Safety API."""

    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        if not self.endpoint or not self.key:
            raise ValueError(
                "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set"
            )
        self.headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json",
        }

    def moderate_text(self, request: TextModerationRequest) -> TextModerationResponse:
        """Moderate text using Azure AI Content Safety."""
        url = f"{self.endpoint}/contentsafety/text:analyze"
        payload = {
            "text": request.text,
            "categories": [cat.value.upper() for cat in request.categories],
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        raw_response = response.json()
        decisions = normalize_azure_scores(raw_response)
        return TextModerationResponse(decisions, raw_response)