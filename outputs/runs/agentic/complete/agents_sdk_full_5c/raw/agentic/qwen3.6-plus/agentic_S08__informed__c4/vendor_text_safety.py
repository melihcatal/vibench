"""
Moderate vendor notes or memo fields using Azure AI Content Safety.

Provider: Azure AI Content Safety
SDK: requests (REST API to Azure Content Safety)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
Endpoint pattern: https://{resource}.cognitiveservices.azure.com/contentSafety/text:analyze
"""

import os
import json
from typing import Dict, Any, List, Optional

import requests

from document_models import InvoiceExtractionResult


AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def moderate_vendor_text(
    text: str,
    hate_severity_threshold: int = 0,
    sexual_severity_threshold: int = 0,
    self_harm_severity_threshold: int = 0,
    violence_severity_threshold: int = 0,
) -> Dict[str, Any]:
    """
    Moderate vendor notes or memo fields using Azure AI Content Safety.

    Analyzes text for hate, sexual, self-harm, and violence categories
    using Azure AI Content Safety text analysis.

    Args:
        text: The text content to moderate.
        hate_severity_threshold: Minimum severity level to flag hate content (0-7).
        sexual_severity_threshold: Minimum severity level to flag sexual content (0-7).
        self_harm_severity_threshold: Minimum severity for self-harm flagging (0-7).
        violence_severity_threshold: Minimum severity for violence flagging (0-7).

    Returns:
        Dictionary with moderation results including safety categories and scores.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise EnvironmentError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY "
            "environment variables are required"
        )

    endpoint = endpoint.rstrip("/")

    url = f"{endpoint}/contentsafety/text:analyze"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "categoriesAnalysis": [
            {"category": "Hate"},
            {"category": "SelfHarm"},
            {"category": "Sexual"},
            {"category": "Violence"},
        ],
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, headers=headers, params=params, json=payload)
    response.raise_for_status()

    result = response.json()
    return _parse_azure_content_safety_response(
        result,
        hate_severity_threshold,
        sexual_severity_threshold,
        self_harm_severity_threshold,
        violence_severity_threshold,
    )


def moderate_vendor_notes_from_invoice(
    extraction_result: InvoiceExtractionResult,
    note_field: str = "vendor_address",
    **thresholds: int,
) -> Dict[str, Any]:
    """
    Extract and moderate vendor-related text from an invoice extraction result.

    Args:
        extraction_result: The invoice extraction result containing vendor fields.
        note_field: Which field to moderate (vendor_address, etc.).
        **thresholds: Severity thresholds for each category.

    Returns:
        Moderation result dictionary.
    """
    raw = extraction_result.raw_response or {}
    text_to_moderate = raw.get(note_field, "")

    if not text_to_moderate:
        text_to_moderate = extraction_result.vendor_name or ""

    if not text_to_moderate:
        return {
            "is_safe": True,
            "text": "",
            "categories": {},
            "provider": "azure_content_safety",
            "note": "No vendor text found to moderate",
        }

    result = moderate_vendor_text(text_to_moderate, **thresholds)
    result["source_field"] = note_field
    return result


def moderate_text_batch(
    texts: List[str],
    **thresholds: int,
) -> List[Dict[str, Any]]:
    """
    Moderate a batch of text inputs using Azure AI Content Safety.

    Args:
        texts: List of text strings to moderate.
        **thresholds: Severity thresholds.

    Returns:
        List of moderation results.
    """
    return [moderate_vendor_text(text, **thresholds) for text in texts]


def _parse_azure_content_safety_response(
    response: Dict[str, Any],
    hate_threshold: int = 0,
    sexual_threshold: int = 0,
    self_harm_threshold: int = 0,
    violence_threshold: int = 0,
) -> Dict[str, Any]:
    """Parse Azure AI Content Safety response into a structured result."""
    categories = {}
    is_safe = True
    flags = []

    thresholds_map = {
        "Hate": hate_threshold,
        "Sexual": sexual_threshold,
        "SelfHarm": self_harm_threshold,
        "Violence": violence_threshold,
    }

    for category_result in response.get("categoriesAnalysis", []):
        category = category_result.get("category", "")
        severity = category_result.get("severity", 0)

        categories[category] = {
            "severity": severity,
            "flagged": severity > thresholds_map.get(category, 0),
        }

        if severity > thresholds_map.get(category, 0):
            is_safe = False
            flags.append({
                "category": category,
                "severity": severity,
                "threshold": thresholds_map.get(category, 0),
            })

    result = {
        "is_safe": is_safe,
        "text": response.get("text", ""),
        "categories": categories,
        "flags": flags,
        "provider": "azure_content_safety",
        "endpoint_domain": "cognitiveservices.azure.com",
    }

    if "blocklistsMatch" in response:
        result["blocklist_matches"] = response["blocklistsMatch"]

    return result
