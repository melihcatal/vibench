"""Checks live transcript text for unsafe content using Azure AI Content Safety."""

import os
from typing import Optional
import requests
from speech_models import StreamingSpeechResult


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://default.cognitiveservices.azure.com/"
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


class ContentSafetyChecker:
    """
    Checks live transcript text for unsafe content using Azure AI Content Safety API.

    Requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.
    Endpoint format: https://{resource}.cognitiveservices.azure.com/
    Uses REST API to {endpoint}/contentsafety/text:analyze.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        hate_threshold: int = 2,
        self_harm_threshold: int = 2,
        sexual_threshold: int = 2,
        violence_threshold: int = 2,
    ):
        self.endpoint = (endpoint or AZURE_CONTENT_SAFETY_ENDPOINT).rstrip("/")
        self.api_key = api_key or AZURE_CONTENT_SAFETY_KEY
        if not self.api_key:
            raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")
        self.thresholds = {
            "Hate": hate_threshold,
            "SelfHarm": self_harm_threshold,
            "Sexual": sexual_threshold,
            "Violence": violence_threshold,
        }

    def analyze_text(self, text: str) -> dict:
        """
        Analyze text content using Azure AI Content Safety text analysis API.

        POSTs to {endpoint}/contentsafety/text:analyze with categories:
        Hate, SelfHarm, Sexual, Violence.
        Uses azure-ai-contentsafety REST endpoint at cognitiveservices.azure.com.
        """
        if not text.strip():
            return {"safe": True, "categories": {}}

        url = f"{self.endpoint}/contentsafety/text:analyze"
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json",
        }
        params = {"api-version": CONTENT_SAFETY_API_VERSION}
        payload = {
            "text": text,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "outputType": "FourSeverityLevels",
        }

        response = requests.post(url, headers=headers, params=params, json=payload)
        response.raise_for_status()
        data = response.json()

        category_scores = {}
        unsafe = False
        for cat_result in data.get("categoriesAnalysis", []):
            category = cat_result.get("category", "")
            severity = cat_result.get("severity", 0)
            category_scores[category] = severity
            if severity >= self.thresholds.get(category, 2):
                unsafe = True

        return {
            "safe": not unsafe,
            "categories": category_scores,
            "raw_response": data,
        }

    def check_result(self, result: StreamingSpeechResult) -> dict:
        """Check a streaming speech result for unsafe content."""
        return self.analyze_text(result.transcript)

    def is_safe(self, text: str) -> bool:
        """Return True if the text passes all safety checks."""
        analysis = self.analyze_text(text)
        return analysis.get("safe", True)


def create_safety_checker(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ContentSafetyChecker:
    """Factory to create a ContentSafetyChecker using Azure AI Content Safety."""
    return ContentSafetyChecker(endpoint=endpoint, api_key=api_key)
