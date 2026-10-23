"""
[LATER-STEP] Moderate vendor notes or memo fields.
Uses Azure AI Content Safety (azure-ai-contentsafety SDK) to analyze and moderate
vendor notes, descriptions, and memo fields from invoices for inappropriate content,
hate speech, violence, or self-harm indicators.

Provider: Azure AI Content Safety
SDK: azure-ai-contentsafety
Endpoint: https://<region>.api.cognitive.microsoft.com/contentsafety
"""

import os
import logging
from typing import Optional, Dict, Any, List

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    TextCategory,
)

from document_models import InvoiceExtractionResult
from document_client import get_azure_content_safety_config, validate_provider_config

logger = logging.getLogger(__name__)

# Azure Content Safety endpoint hostname
AZURE_CONTENT_SAFETY_HOST = "api.cognitive.microsoft.com/contentsafety"

# Safety thresholds (0-7 scale, where higher is more severe)
DEFAULT_SAFETY_THRESHOLD = 2


def moderate_vendor_text(
    text: str,
    threshold: int = DEFAULT_SAFETY_THRESHOLD,
) -> Dict[str, Any]:
    """
    Moderate vendor notes or memo text using Azure AI Content Safety.

    Args:
        text: Text content to moderate (vendor notes, descriptions, memos).
        threshold: Safety threshold (0-7 scale, default 2).

    Returns:
        Dictionary with moderation results including safety scores and flags.
    """
    config = get_azure_content_safety_config()
    if not validate_provider_config("azure_content_safety", config):
        raise ValueError("Azure Content Safety configuration is incomplete. "
                        "Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY.")

    endpoint = config["endpoint"]
    api_key = config["api_key"]

    try:
        # Initialize Azure Content Safety client
        credential = AzureKeyCredential(api_key)
        client = ContentSafetyClient(
            endpoint=endpoint,
            credential=credential,
        )

        logger.info(f"Analyzing text safety with Azure Content Safety: {AZURE_CONTENT_SAFETY_HOST}")

        # Build text analysis request
        analysis_options = AnalyzeTextOptions(
            text=text,
            categories=[
                TextCategory.HATE,
                TextCategory.SELF_HARM,
                TextCategory.SEXUAL,
                TextCategory.VIOLENCE,
            ],
        )

        # Call Azure Content Safety API
        analysis_result = client.analyze_text(analysis_options)

        # Parse moderation results
        moderation_result = {
            "text_length": len(text),
            "is_safe": True,
            "categories": {},
            "max_severity": 0,
            "flagged_categories": [],
        }

        for category_result in analysis_result.categories_analysis:
            category_name = category_result.category.value if hasattr(category_result.category, "value") else str(category_result.category)
            severity = category_result.severity or 0

            moderation_result["categories"][category_name] = severity
            moderation_result["max_severity"] = max(
                moderation_result["max_severity"], severity
            )

            if severity > threshold:
                moderation_result["is_safe"] = False
                moderation_result["flagged_categories"].append(category_name)

        return moderation_result

    except Exception as e:
        logger.error(f"Azure Content Safety moderation error: {str(e)}")
        raise


def moderate_vendor_notes_from_invoice(
    invoice: InvoiceExtractionResult,
    threshold: int = DEFAULT_SAFETY_THRESHOLD,
) -> Dict[str, Any]:
    """
    Moderate vendor notes and memo fields from an extracted invoice.

    Args:
        invoice: InvoiceExtractionResult containing vendor notes/memos.
        threshold: Safety threshold for moderation.

    Returns:
        Dictionary with moderation results for invoice notes.
    """
    # Collect all text fields that may contain notes
    text_fields = []

    # Check raw response for memo/notes fields
    if invoice.raw_response and isinstance(invoice.raw_response, dict):
        memo = invoice.raw_response.get("memo", "")
        notes = invoice.raw_response.get("notes", "")
        vendor_notes = invoice.raw_response.get("vendor_notes", "")

        if memo:
            text_fields.append(("memo", memo))
        if notes:
            text_fields.append(("notes", notes))
        if vendor_notes:
            text_fields.append(("vendor_notes", vendor_notes))

    # If no notes found in raw response, check vendor name and line item descriptions
    if not text_fields:
        if invoice.vendor and len(invoice.vendor) > 50:
            text_fields.append(("vendor_description", invoice.vendor))

        for item in invoice.line_items[:5]:
            if item.description and len(item.description) > 20:
                text_fields.append(("line_item", item.description))

    # Moderate each text field
    all_results = {
        "invoice_number": invoice.invoice_number,
        "vendor": invoice.vendor,
        "overall_safe": True,
        "field_results": {},
    }

    for field_name, text in text_fields:
        try:
            result = moderate_vendor_text(text, threshold=threshold)
            all_results["field_results"][field_name] = result
            if not result["is_safe"]:
                all_results["overall_safe"] = False
        except Exception as e:
            logger.error(f"Failed to moderate field '{field_name}': {str(e)}")
            all_results["field_results"][field_name] = {
                "error": str(e),
                "is_safe": True,  # Default to safe on error
            }

    return all_results


def moderate_vendor_memo(memo_text: str) -> Dict[str, Any]:
    """
    Moderate a single vendor memo string using Azure Content Safety.

    Args:
        memo_text: Vendor memo or note text to moderate.

    Returns:
        Moderation result dictionary.
    """
    return moderate_vendor_text(memo_text, threshold=DEFAULT_SAFETY_THRESHOLD)
