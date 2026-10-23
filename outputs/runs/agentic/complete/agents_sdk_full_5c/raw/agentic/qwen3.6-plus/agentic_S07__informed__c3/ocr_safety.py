"""
Check extracted document text for unsafe content using Azure AI Content Safety.

Uses the Azure AI Content Safety REST API via requests to analyze text for
hate speech, self-harm, sexual content, and violence.
"""

import os
from typing import Dict, Optional

import requests


AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"

CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def get_azure_content_safety_endpoint() -> str:
    endpoint = os.environ.get(AZURE_CONTENT_SAFETY_ENDPOINT_ENV)
    if not endpoint:
        raise ValueError(
            f"Missing required environment variable: {AZURE_CONTENT_SAFETY_ENDPOINT_ENV}"
        )
    return endpoint


def get_azure_content_safety_key() -> str:
    key = os.environ.get(AZURE_CONTENT_SAFETY_KEY_ENV)
    if not key:
        raise ValueError(
            f"Missing required environment variable: {AZURE_CONTENT_SAFETY_KEY_ENV}"
        )
    return key


def check_ocr_text_safety(
    text: str,
    *,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
    output_type: str = "FourSeverityLevels",
) -> Dict:
    """
    Analyze extracted OCR text for unsafe content using Azure AI Content Safety.

    Args:
        text: The OCR-extracted text to analyze.
        endpoint: Azure Content Safety endpoint URL.
            Falls back to AZURE_CONTENT_SAFETY_ENDPOINT.
        key: Azure Content Safety API key.
            Falls back to AZURE_CONTENT_SAFETY_KEY.
        output_type: Response format. "FourSeverityLevels" or "EightSeverityLevels".

    Returns:
        Dict with safety analysis results including categories
        (hate, selfHarm, sexual, violence) and severity levels.
    """
    ep = endpoint or get_azure_content_safety_endpoint()
    ak = key or get_azure_content_safety_key()

    url = f"{ep}/contentsafety/text:analyze?api-version={CONTENT_SAFETY_API_VERSION}"
    headers = {
        "Ocp-Apim-Subscription-Key": ak,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "outputType": output_type,
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


def is_text_safe(
    text: str,
    *,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
    max_severity: int = 2,
) -> bool:
    """
    Determine whether OCR-extracted text is safe (all categories below max_severity).

    Args:
        text: The text to check.
        max_severity: Maximum allowed severity level (0-7 for EightSeverityLevels,
                      0-4 for FourSeverityLevels). Default is 2.
        endpoint: Azure Content Safety endpoint URL.
        key: Azure Content Safety API key.

    Returns:
        True if all category severities are <= max_severity, False otherwise.
    """
    result = check_ocr_text_safety(text, endpoint=endpoint, key=key)
    categories = result.get("categoriesAnalysis", [])
    for cat in categories:
        severity = cat.get("severity", 0)
        if severity > max_severity:
            return False
    return True


if __name__ == "__main__":
    sample_text = "This is a safe document about recipes and cooking."
    result = check_ocr_text_safety(sample_text)
    print(result)
