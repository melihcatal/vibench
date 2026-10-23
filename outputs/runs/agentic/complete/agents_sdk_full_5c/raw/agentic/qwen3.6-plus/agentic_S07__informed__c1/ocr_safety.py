"""Check extracted document text for unsafe content using Azure AI Content Safety."""

import os
import requests

from document_models import SafetyCheckRequest, SafetyCheckResponse, SafetyFlag


class AzureContentSafetyChecker:
    """Content safety analysis via Azure AI Content Safety REST API."""

    def __init__(self):
        self.endpoint = os.environ.get(
            "AZURE_CONTENT_SAFETY_ENDPOINT",
            "https://<your-resource>.cognitiveservices.azure.com/",
        ).rstrip("/")
        self.api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
        self.api_version = "2024-02-15-preview"
        self.analyze_url = f"{self.endpoint}/contentsafety/text:analyze?api-version={self.api_version}"

    def analyze_text(
        self,
        text: str,
        categories: list[str] | None = None,
    ) -> SafetyCheckResponse:
        """Send text to Azure AI Content Safety for moderation analysis."""
        if not self.api_key:
            raise EnvironmentError("Missing AZURE_CONTENT_SAFETY_KEY environment variable.")

        if categories is None:
            categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

        payload = {
            "text": text,
            "categories": categories,
            "outputType": "FourSeverityLevels",
        }

        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json",
        }

        response = requests.post(self.analyze_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        flags = []
        overall_safe = True

        for category_result in data.get("categoriesAnalysis", []):
            category = category_result.get("category", "")
            severity = category_result.get("severity", 0)

            severity_labels = {0: "Safe", 2: "Low", 4: "Medium", 6: "High"}
            severity_str = severity_labels.get(severity, f"Unknown({severity})")

            flagged = severity > 0
            if flagged:
                overall_safe = False

            flags.append(
                SafetyFlag(
                    category=category,
                    score=float(severity),
                    severity=severity_str,
                    flagged=flagged,
                )
            )

        return SafetyCheckResponse(
            flags=flags,
            overall_safe=overall_safe,
            provider="azure-ai-content-safety",
        )


def check_safety(text: str, categories: list[str] | None = None) -> SafetyCheckResponse:
    """High-level helper: check extracted OCR text for unsafe content via Azure AI Content Safety."""
    checker = AzureContentSafetyChecker()
    return checker.analyze_text(text, categories=categories)


def check_safety_batch(texts: list[str], categories: list[str] | None = None) -> list[SafetyCheckResponse]:
    """High-level helper: check multiple OCR text segments for unsafe content via Azure AI Content Safety."""
    checker = AzureContentSafetyChecker()
    results = []
    for text in texts:
        results.append(checker.analyze_text(text, categories=categories))
    return results
