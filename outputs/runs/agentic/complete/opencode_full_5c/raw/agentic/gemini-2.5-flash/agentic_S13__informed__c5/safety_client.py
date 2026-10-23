import os
from typing import Dict, Any, List
import requests
from safety_models import (
    TextModerationRequest,
    TextModerationResponse,
    TextRedactionRequest,
    TextRedactionResponse,
)

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY")


class AzureSafetyClient:
    def __init__(self):
        if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
            raise ValueError(
                "Azure Content Safety endpoint and key must be set in environment variables."
            )
        self.endpoint = AZURE_CONTENT_SAFETY_ENDPOINT
        self.key = AZURE_CONTENT_SAFETY_KEY

    def moderate_text(self, request: TextModerationRequest) -> TextModerationResponse:
        url = (
            f"{self.endpoint}/contentsafety/text:analyze?api-version=2023-10-01-preview"
        )
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json",
        }
        payload = {
            "text": request.text,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "outputType": "FourSeverityLevels",
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        categories_analysis = {}
        for category in data.get("categoriesAnalysis", []):
            categories_analysis[category["category"]] = {
                "severity": category["severity"]
            }

        block_id = None  # Azure AI Content Safety doesn't return a block ID directly for text moderation

        return TextModerationResponse(
            categories_analysis=categories_analysis, block_id=block_id
        )

    def moderate_batch(
        self, requests: List[TextModerationRequest]
    ) -> List[TextModerationResponse]:
        responses = []
        for req in requests:
            responses.append(self.moderate_text(req))
        return responses

    def redact_unsafe(self, request: TextRedactionRequest) -> TextRedactionResponse:
        url = (
            f"{self.endpoint}/contentsafety/text:analyze?api-version=2023-10-01-preview"
        )
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json",
        }
        payload = {
            "text": request.text,
            "blocklistNames": [],  # No specific blocklist for general redaction
            "breakByCharacters": True,
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Azure AI Content Safety doesn't provide a direct 'redactedText' output for all categories.
        # A more robust redaction would involve checking each category's severity and then replacing.
        # For this example, we'll assume a simple pass-through or a placeholder if a high severity is detected.
        # In a real scenario, you'd integrate with a redaction-specific feature if available or implement based on offsets.
        redacted_text = request.text  # Placeholder
        for category_analysis in data.get("categoriesAnalysis", []):
            if category_analysis.get("severity", 0) > 0:
                # This is a simplification. Real redaction needs span information, which Azure Content Safety can provide
                # but requires more complex parsing and text manipulation.
                redacted_text = "[REDACTED]"
                break

        return TextRedactionResponse(redacted_text=redacted_text)
