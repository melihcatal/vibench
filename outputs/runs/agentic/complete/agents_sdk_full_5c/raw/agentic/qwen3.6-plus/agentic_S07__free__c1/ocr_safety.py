"""
ocr_safety.py - Checks extracted document text for unsafe content
using Azure AI Content Safety.

Provider: Azure AI Content Safety
SDK: azure-ai-contentsafety
Endpoint: api.cognitiveservices.azure.com / contentsafety.cognitiveservices.azure.com
"""

import os
from typing import List, Optional

from document_models import (
    ExtractTextResponse,
    SafetyCheckRequest,
    SafetyCheckResponse,
    SafetyResult,
)

PROVIDER = "azure-content-safety"
AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def _normalize_endpoint(endpoint: str) -> str:
    """Normalize the Content Safety endpoint URL."""
    if not endpoint.startswith("https://"):
        endpoint = f"https://{endpoint}"
    if not endpoint.endswith("/"):
        endpoint += "/"
    return endpoint


def check_content_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    """
    Check extracted document text for unsafe content categories
    using Azure AI Content Safety's text analysis API.

    Args:
        request: SafetyCheckRequest with text to analyze and optional categories.

    Returns:
        SafetyCheckResponse with safety results per category.
    """
    import http.client
    import json

    if not request.text:
        raise ValueError("Text is required for safety analysis.")

    if not AZURE_CONTENT_SAFETY_KEY:
        raise EnvironmentError(
            "AZURE_CONTENT_SAFETY_KEY environment variable is required."
        )

    normalized_endpoint = _normalize_endpoint(AZURE_CONTENT_SAFETY_ENDPOINT)
    host = normalized_endpoint.replace("https://", "").rstrip("/")
    route = f"/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"

    # Azure Content Safety categories
    default_categories = ["Hate", "SelfHarm", "Sexual", "Violence"]
    categories = request.categories if request.categories else default_categories

    body = json.dumps({
        "text": request.text,
        "categories": categories,
    })

    conn = http.client.HTTPSConnection(host)

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
        "Content-Length": str(len(body)),
    }

    conn.request("POST", route, body=body, headers=headers)
    response = conn.getresponse()
    response_data = response.read().decode("utf-8")
    conn.close()

    result = json.loads(response_data)

    safety_results: List[SafetyResult] = []
    overall_safe = True

    for cat_result in result.get("categoriesAnalysis", []):
        category = cat_result.get("category", "Unknown")
        severity = cat_result.get("severity", 0)
        flagged = severity > 0

        safety_result = SafetyResult(
            category=category,
            severity=severity,
            flagged=flagged,
        )
        safety_results.append(safety_result)

        if flagged:
            overall_safe = False

    return SafetyCheckResponse(
        overall_safe=overall_safe,
        results=safety_results,
        provider=PROVIDER,
        raw_response={"status": response.status, "body": result},
    )


def check_ocr_safety(ocr_response: ExtractTextResponse) -> SafetyCheckResponse:
    """
    Check the full text from an OCR extraction for unsafe content.

    Args:
        ocr_response: ExtractTextResponse from OCR extraction.

    Returns:
        SafetyCheckResponse with safety analysis results.
    """
    req = SafetyCheckRequest(text=ocr_response.full_text)
    return check_content_safety(req)


def check_document_safety(
    text: str,
    categories: Optional[List[str]] = None,
) -> SafetyCheckResponse:
    """
    Convenience function to check arbitrary document text for unsafe content.

    Args:
        text: The text to analyze.
        categories: Optional list of categories to check.

    Returns:
        SafetyCheckResponse with safety analysis results.
    """
    req = SafetyCheckRequest(text=text, categories=categories)
    return check_content_safety(req)
