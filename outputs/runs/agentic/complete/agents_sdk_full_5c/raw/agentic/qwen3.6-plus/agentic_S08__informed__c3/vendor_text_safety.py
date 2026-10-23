"""Moderate vendor notes or memo fields using Azure AI Content Safety.

Uses Azure AI Content Safety REST API to check vendor text for harmful,
hate, self-harm, sexual, and violent content categories.
Auth env vars: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
import json
from typing import Optional
import requests
from document_models import InvoiceExtractionResult


CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def moderate_vendor_text(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> dict:
    """Moderate vendor notes or memo text using Azure AI Content Safety.

    Calls the Azure AI Content Safety Text: Analyze endpoint to detect
    harmful content across multiple categories.

    Args:
        text: The vendor note or memo text to moderate.
        endpoint: Azure Content Safety endpoint URL.
        api_key: Azure Content Safety API key.

    Returns:
        Dictionary with moderation results including category scores.
    """
    if endpoint is None:
        endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    if api_key is None:
        api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

    if not endpoint:
        raise EnvironmentError("AZURE_CONTENT_SAFETY_ENDPOINT environment variable is not set")
    if not api_key:
        raise EnvironmentError("AZURE_CONTENT_SAFETY_KEY environment variable is not set")

    # Ensure endpoint has the right format for the API
    base_url = endpoint.rstrip("/")
    url = f"{base_url}/contentsafety/text:analyze?api-version={CONTENT_SAFETY_API_VERSION}"

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key,
    }

    payload = {
        "text": text,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()

    category_scores = {}
    for category_result in result.get("categoriesAnalysis", []):
        category = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        category_scores[category] = severity

    is_safe = all(severity <= 2 for severity in category_scores.values())

    return {
        "text_analyzed": text,
        "category_scores": category_scores,
        "is_safe": is_safe,
        "max_severity": max(category_scores.values()) if category_scores else 0,
        "raw_response": result,
    }


def moderate_vendor_from_invoice(
    extraction: InvoiceExtractionResult,
) -> dict:
    """Moderate any notes or memos found in an extracted invoice.

    Uses Azure AI Content Safety to check vendor-related text fields.
    """
    vendor_text = extraction.raw_fields.get("VendorName", extraction.vendor_name)

    notes = extraction.raw_fields.get("Notes", "")
    memo = extraction.raw_fields.get("Memo", "")

    combined_text = " ".join(
        part for part in [vendor_text, notes, memo] if part
    ).strip()

    if not combined_text:
        return {
            "text_analyzed": "",
            "category_scores": {},
            "is_safe": True,
            "max_severity": 0,
            "raw_response": {},
            "note": "No text content to moderate",
        }

    return moderate_vendor_text(combined_text)


if __name__ == "__main__":
    import sys
    sample_text = sys.argv[1] if len(sys.argv) > 1 else "Sample vendor note for moderation testing."
    result = moderate_vendor_text(sample_text)
    print(json.dumps(result, indent=2))
