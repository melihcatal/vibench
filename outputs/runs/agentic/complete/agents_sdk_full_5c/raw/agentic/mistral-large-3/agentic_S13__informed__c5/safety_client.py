# Local configuration and client helper utilities for Text Content Safety

import os
from typing import Optional, Dict, List
import requests
from safety_models import SafetyCategory, TextModerationRequest, TextModerationResponse, RedactionResponse, normalize_safety_decision


class AzureContentSafetyClient:
    """Client for Azure AI Content Safety service."""

    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        if not self.endpoint or not self.key:
            raise ValueError("Azure Content Safety environment variables not set.")
        self.headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json",
        }

    def moderate_text(self, request: TextModerationRequest) -> TextModerationResponse:
        """Moderate text using Azure AI Content Safety."""
        url = f"{self.endpoint}/contentsafety/text:analyze"
        payload = {
            "text": request["text"],
            "categories": [c.value.upper() for c in request.get("categories", list(SafetyCategory))],
            "outputType": "FourSeverityLevels",
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        raw_response = response.json()

        decisions = []
        for cat in raw_response.get("categoriesAnalysis", []):
            category = SafetyCategory(cat["category"].lower())
            score = cat["severity"] / 4.0  # Normalize 0-4 to 0-1
            decisions.append(normalize_safety_decision({
                "category": category,
                "score": score,
                "threshold": 0.5,
            }, request.get("threshold_overrides")))

        return {
            "decisions": decisions,
            "raw_response": raw_response,
        }

    def redact_unsafe(self, request: TextModerationRequest) -> RedactionResponse:
        """Redact unsafe spans using Azure AI Content Safety."""
        url = f"{self.endpoint}/contentsafety/text:redact"
        payload = {
            "text": request["text"],
            "categories": [c.value.upper() for c in request.get("categories", list(SafetyCategory))],
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        raw_response = response.json()

        spans = []
        redacted_text = raw_response["redactedText"]
        for cat in raw_response.get("categoriesAnalysis", []):
            category = SafetyCategory(cat["category"].lower())
            for span in cat.get("filteredSpans", []):
                spans.append({
                    "start": span["offset"],
                    "end": span["offset"] + span["length"],
                    "category": category,
                    "replacement": "*" * (span["length"]),
                })

        return {
            "redacted_text": redacted_text,
            "spans": spans,
            "raw_response": raw_response,
        }