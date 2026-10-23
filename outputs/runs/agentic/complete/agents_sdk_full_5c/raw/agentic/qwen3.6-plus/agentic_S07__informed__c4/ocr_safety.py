"""
[LATER-STEP] Check extracted document text for unsafe content.

Provider: Azure AI Content Safety
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
Service endpoint: cognitiveservices.azure.com (Azure Content Safety)
"""

from __future__ import annotations

import os
from typing import Optional, Dict, Any, List
import requests

from document_client import get_azure_content_safety_endpoint, get_azure_content_safety_key
from document_models import SafetyAnalysisResult, OcrDocumentResult


# Azure AI Content Safety categories map
CONTENT_SAFETY_CATEGORIES = [
    "Hate",
    "SelfHarm",
    "Sexual",
    "Violence",
]


def check_ocr_safety(
    ocr_result: OcrDocumentResult,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: str = "2024-09-01",
) -> SafetyAnalysisResult:
    """
    Analyze extracted OCR text for unsafe content using
    Azure AI Content Safety REST API (cognitiveservices.azure.com).

    Uses the concrete Azure Content Safety Text:Analyze endpoint
    with categories: Hate, SelfHarm, Sexual, Violence.
    """
    endpoint = endpoint or get_azure_content_safety_endpoint()
    api_key = api_key or get_azure_content_safety_key()

    if not endpoint:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT environment variable or endpoint argument is required"
        )
    if not api_key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_KEY environment variable or api_key argument is required"
        )

    text = ocr_result.plain_text
    if not text:
        return SafetyAnalysisResult(text_analyzed="", is_safe=True)

    # Azure Content Safety Text Analyze endpoint
    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key,
    }

    payload = {
        "text": text,
        "categories": CONTENT_SAFETY_CATEGORIES,
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    data = response.json()
    return _parse_safety_response(text, data)


def _parse_safety_response(
    text: str,
    response_data: Dict[str, Any],
) -> SafetyAnalysisResult:
    """Parse Azure Content Safety API response into SafetyAnalysisResult."""
    categories: Dict[str, float] = {}
    flags: List[str] = []
    is_safe = True

    for category_result in response_data.get("categoriesAnalysis", []):
        cat_name = category_result.get("category", "Unknown")
        severity = category_result.get("severity", 0)
        categories[cat_name] = severity
        if severity >= 2:
            flags.append(cat_name)
            is_safe = False

    return SafetyAnalysisResult(
        text_analyzed=text,
        categories=categories,
        is_safe=is_safe,
        flags=flags,
    )


def check_text_safety(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: str = "2024-09-01",
) -> SafetyAnalysisResult:
    """
    Analyze arbitrary text for unsafe content using Azure AI Content Safety
    REST API (cognitiveservices.azure.com).
    """
    endpoint = endpoint or get_azure_content_safety_endpoint()
    api_key = api_key or get_azure_content_safety_key()

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety endpoint and key are required")

    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key,
    }

    payload = {
        "text": text,
        "categories": CONTENT_SAFETY_CATEGORIES,
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    data = response.json()
    return _parse_safety_response(text, data)
