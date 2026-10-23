"""
Check user-generated document fields for unsafe content using Azure AI Content Safety.

Provider: Azure AI Content Safety
SDK: requests (REST API)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
Interface: REST
"""

import json
import os
from typing import Any, Dict, List, Optional

import requests


_AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def _build_text_analysis_payload(
    text: str,
    categories: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build the request payload for Azure AI Content Safety text analysis."""
    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]
    return {
        "text": text,
        "categories": categories,
        "outputType": "FourSeverityLevels",
    }


def check_text_safety(
    text: str,
    categories: Optional[List[str]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Analyze user-generated text for unsafe content via Azure AI Content Safety.

    Sends the text to the Azure Content Safety Text: Analyze API endpoint
    and returns severity levels for each category.

    Args:
        text: The text content to analyze for safety.
        categories: List of categories to check (Hate, SelfHarm, Sexual, Violence).
        endpoint: Optional override for AZURE_CONTENT_SAFETY_ENDPOINT.
        api_key: Optional override for AZURE_CONTENT_SAFETY_KEY.

    Returns:
        A dict with safety analysis results including per-category severity.
    """
    service_endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    service_key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not service_endpoint:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT is required for Azure AI Content Safety."
        )
    if not service_key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_KEY is required for Azure AI Content Safety."
        )

    # Normalize endpoint - remove trailing slash
    service_endpoint = service_endpoint.rstrip("/")

    url = (
        f"{service_endpoint}/contentsafety/text:analyze"
        f"?api-version={_AZURE_CONTENT_SAFETY_API_VERSION}"
    )

    headers = {
        "Ocp-Apim-Subscription-Key": service_key,
        "Content-Type": "application/json",
    }

    payload = _build_text_analysis_payload(text, categories=categories)

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()

    category_results = {}
    for category_result in result.get("categoriesAnalysis", []):
        category = category_result.get("category", "Unknown")
        severity = category_result.get("severity", 0)
        category_results[category] = severity

    is_safe = all(sev == 0 for sev in category_results.values())

    return {
        "is_safe": is_safe,
        "categories": category_results,
        "text_length": len(text),
        "blocklists_match": result.get("blocklistsMatch", []),
    }


def check_document_fields_safety(
    document: Dict[str, Any],
    text_fields: Optional[List[str]] = None,
    categories: Optional[List[str]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Check multiple text fields within a document for unsafe content.

    Args:
        document: The document containing text fields to check.
        text_fields: List of field names to check. Defaults to common user-content fields.
        categories: Safety categories to evaluate.
        endpoint: Optional Azure Content Safety endpoint override.
        api_key: Optional Azure Content Safety key override.

    Returns:
        A dict with per-field safety results and an overall safety verdict.
    """
    if text_fields is None:
        text_fields = ["content", "description", "title", "body", "comment", "message"]

    field_results = {}
    overall_safe = True

    for field_name in text_fields:
        field_value = document.get(field_name)
        if field_value is not None and isinstance(field_value, str):
            result = check_text_safety(
                text=field_value,
                categories=categories,
                endpoint=endpoint,
                api_key=api_key,
            )
            field_results[field_name] = result
            if not result["is_safe"]:
                overall_safe = False

    return {
        "document_safe": overall_safe,
        "field_results": field_results,
        "fields_checked": list(field_results.keys()),
    }
