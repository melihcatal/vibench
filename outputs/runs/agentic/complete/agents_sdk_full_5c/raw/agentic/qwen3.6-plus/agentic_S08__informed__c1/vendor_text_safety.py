"""
[LATER-STEP] Moderate vendor notes or memo fields using Azure AI Content Safety.

Uses the Azure AI Content Safety API to analyze vendor notes, invoice memos,
and free-text fields extracted from invoices/receipts for inappropriate content.
Provider: Azure AI Content Safety
SDK: requests (REST) / azure-ai-contentsafety compatible
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import requests

from document_models import (
    InvoiceExtractionResult,
    ReceiptExtractionResult,
)


# Azure AI Content Safety configuration
AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"
CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def _get_content_safety_config() -> tuple:
    """Retrieve Azure Content Safety endpoint and key from environment."""
    endpoint = os.environ.get(AZURE_CONTENT_SAFETY_ENDPOINT_ENV)
    key = os.environ.get(AZURE_CONTENT_SAFETY_KEY_ENV)

    if not endpoint:
        raise EnvironmentError(
            f"Azure Content Safety endpoint not found. Set {AZURE_CONTENT_SAFETY_ENDPOINT_ENV}."
        )
    if not key:
        raise EnvironmentError(
            f"Azure Content Safety key not found. Set {AZURE_CONTENT_SAFETY_KEY_ENV}."
        )

    # Normalize endpoint (remove trailing slash)
    endpoint = endpoint.rstrip("/")
    return endpoint, key


def moderate_text(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Moderate text content using Azure AI Content Safety API.

    Analyzes text for hate, self-harm, sexual, and violence categories.

    Args:
        text: The text to moderate.
        endpoint: Optional Azure Content Safety endpoint override.
        api_key: Optional Azure Content Safety API key override.

    Returns:
        Dictionary with moderation results including category scores and overall verdict.
    """
    if endpoint is None or api_key is None:
        endpoint, api_key = _get_content_safety_config()

    url = f"{endpoint}/contentsafety/text:analyze?api-version={CONTENT_SAFETY_API_VERSION}"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    return result


def moderate_vendor_notes(
    invoice: InvoiceExtractionResult,
    notes_field: str = "notes",
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Moderate vendor notes/memo fields from an invoice using Azure AI Content Safety.

    Checks any text extracted as vendor notes or invoice memos for policy violations.

    Args:
        invoice: InvoiceExtractionResult from Mindee Invoice OCR.
        notes_field: Field name in raw_fields to check for notes.
        endpoint: Optional Azure Content Safety endpoint.
        api_key: Optional Azure Content Safety API key.

    Returns:
        Moderation result dictionary with category severities and recommendation.
    """
    # Check for notes in the invoice object
    notes_text = ""
    if hasattr(invoice, "notes") and invoice.notes:
        notes_text = invoice.notes
    elif invoice.raw_fields and notes_field in invoice.raw_fields:
        notes_text = str(invoice.raw_fields[notes_field])

    # Also check vendor notes/memo fields from Mindee raw extraction
    raw = invoice.raw_fields
    for key in ["notes", "memo", "vendor_notes", "comments", "description"]:
        if key in raw and raw[key]:
            if notes_text:
                notes_text += " " + str(raw[key])
            else:
                notes_text = str(raw[key])

    if not notes_text.strip():
        return {
            "text_analyzed": "",
            "is_safe": True,
            "categories": [],
            "recommendation": "NO_CONTENT",
            "message": "No vendor notes or memo text found to moderate.",
        }

    result = moderate_text(notes_text, endpoint=endpoint, api_key=api_key)

    # Parse Azure Content Safety response
    analysis_result = result.get("analysisResult", {})
    categories_analysis = analysis_result.get("categoriesAnalysis", [])

    category_scores = {}
    for cat in categories_analysis:
        category_scores[cat.get("category", "Unknown")] = cat.get("severity", 0)

    # Determine overall safety verdict
    max_severity = max((cat.get("severity", 0) for cat in categories_analysis), default=0)
    is_safe = max_severity <= 2  # Azure severity 0-2 is generally safe

    recommendation = "PASS" if is_safe else "REVIEW"
    if max_severity >= 6:
        recommendation = "BLOCK"

    return {
        "text_analyzed": notes_text[:500],
        "is_safe": is_safe,
        "categories": category_scores,
        "max_severity": max_severity,
        "recommendation": recommendation,
        "provider": "Azure AI Content Safety",
    }


def moderate_receipt_memo(
    receipt: ReceiptExtractionResult,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Moderate memo/notes fields from a receipt using Azure AI Content Safety.

    Args:
        receipt: ReceiptExtractionResult from Mindee Receipt OCR.
        endpoint: Optional Azure Content Safety endpoint.
        api_key: Optional Azure Content Safety API key.

    Returns:
        Moderation result dictionary.
    """
    notes_text = ""
    if hasattr(receipt, "notes") and receipt.notes:
        notes_text = receipt.notes
    elif receipt.raw_fields:
        for key in ["notes", "memo", "comments"]:
            if key in receipt.raw_fields and receipt.raw_fields[key]:
                notes_text = str(receipt.raw_fields[key])
                break

    if not notes_text.strip():
        return {
            "text_analyzed": "",
            "is_safe": True,
            "categories": [],
            "recommendation": "NO_CONTENT",
            "message": "No receipt memo text found to moderate.",
        }

    result = moderate_text(notes_text, endpoint=endpoint, api_key=api_key)

    analysis_result = result.get("analysisResult", {})
    categories_analysis = analysis_result.get("categoriesAnalysis", [])

    category_scores = {}
    for cat in categories_analysis:
        category_scores[cat.get("category", "Unknown")] = cat.get("severity", 0)

    max_severity = max((cat.get("severity", 0) for cat in categories_analysis), default=0)
    is_safe = max_severity <= 2

    recommendation = "PASS" if is_safe else "REVIEW"
    if max_severity >= 6:
        recommendation = "BLOCK"

    return {
        "text_analyzed": notes_text[:500],
        "is_safe": is_safe,
        "categories": category_scores,
        "max_severity": max_severity,
        "recommendation": recommendation,
        "provider": "Azure AI Content Safety",
    }


def batch_moderate_texts(
    texts: List[str],
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Moderately multiple text inputs using Azure AI Content Safety in batch.

    Args:
        texts: List of text strings to moderate.
        endpoint: Optional Azure Content Safety endpoint.
        api_key: Optional Azure Content Safety API key.

    Returns:
        List of moderation results, one per input text.
    """
    if endpoint is None or api_key is None:
        endpoint, api_key = _get_content_safety_config()

    url = f"{endpoint}/contentsafety/text:analyze?api-version={CONTENT_SAFETY_API_VERSION}"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": " ".join(texts),
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    return [result]
