"""
Check message payload text for unsafe content using Azure AI Content Safety.

Uses the azure-ai-contentsafety SDK to analyze text for harmful content
including hate speech, self-harm, sexual content, and violence.
Requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.
"""

import os
import json
from typing import Optional

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError


class SafetyAnalysisResult:
    """Result of a content safety analysis."""

    def __init__(self, text: str):
        self.text = text
        self.is_safe = True
        self.categories: dict = {}
        self.severity_scores: dict = {}
        self.error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "text_length": len(self.text),
            "is_safe": self.is_safe,
            "categories": self.categories,
            "severity_scores": self.severity_scores,
            "error": self.error,
        }


def check_message_safety(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> SafetyAnalysisResult:
    """
    Check message payload text for unsafe content using Azure AI Content Safety.

    Analyzes text across categories: Hate, SelfHarm, Sexual, Violence.

    Args:
        text: The message text to analyze.
        endpoint: Azure Content Safety endpoint URL.
        api_key: Azure Content Safety API key.

    Returns:
        SafetyAnalysisResult with safety assessment.
    """
    result = SafetyAnalysisResult(text=text)

    try:
        az_endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
        az_key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

        if not az_endpoint or not az_key:
            result.is_safe = False
            result.error = "Azure Content Safety credentials not configured"
            return result

        credential = AzureKeyCredential(az_key)
        client = ContentSafetyClient(
            endpoint=az_endpoint,
            credential=credential,
        )

        categories = [
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ]

        request = AnalyzeTextOptions(text=text, categories=categories)
        response = client.analyze_text(request)

        all_safe = True
        for analysis in response.categories_analysis:
            category_name = str(analysis.category).split(".")[-1]
            severity = analysis.severity or 0
            result.severity_scores[category_name] = severity

            if severity > 0:
                all_safe = False
                result.categories[category_name] = {
                    "severity": severity,
                    "flagged": severity >= 4,
                }

        result.is_safe = all_safe

    except HttpResponseError as e:
        result.is_safe = False
        result.error = f"Azure Content Safety API error: {str(e)}"
    except Exception as e:
        result.is_safe = False
        result.error = f"Unexpected error: {str(e)}"

    return result


def is_message_safe(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> bool:
    """
    Quick check if message text is safe.

    Args:
        text: The message text to check.
        endpoint: Azure Content Safety endpoint.
        api_key: Azure Content Safety API key.

    Returns:
        True if the message is safe, False otherwise.
    """
    result = check_message_safety(text, endpoint=endpoint, api_key=api_key)
    return result.is_safe


if __name__ == "__main__":
    sample_text = "This is a normal message about a product update."
    result = check_message_safety(sample_text)
    print(json.dumps(result.to_dict(), indent=2))
