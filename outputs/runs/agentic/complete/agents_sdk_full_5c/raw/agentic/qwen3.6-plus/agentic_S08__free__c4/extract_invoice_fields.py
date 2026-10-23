"""
[SAME-SCENARIO] Extract vendor, date, total, and line-item fields from an invoice.
Uses Azure AI Document Intelligence (azure-ai-documentintelligence SDK) with the
prebuilt-invoice model to extract structured invoice data from PDF or image files.

Provider: Azure AI Document Intelligence
SDK: azure-ai-documentintelligence
Model: prebuilt-invoice
"""

import os
import logging
from typing import Optional, Dict, Any

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_models import InvoiceExtractionResult, InvoiceLineItem, ConfidenceScore
from document_client import get_azure_ai_client_config, validate_provider_config

logger = logging.getLogger(__name__)


# Azure AI Document Intelligence uses the prebuilt-invoice model
AZURE_INVOICE_MODEL_ID = "prebuilt-invoice"


def extract_invoice_fields(
    document_bytes: bytes,
    content_type: str = "application/pdf",
    locale: str = "en-US",
) -> InvoiceExtractionResult:
    """
    Extract vendor, date, total, and line-item fields from an invoice document
    using Azure AI Document Intelligence prebuilt-invoice model.

    Args:
        document_bytes: Raw bytes of the invoice document (PDF or image).
        content_type: MIME type of the document (default: application/pdf).
        locale: Document locale for parsing (default: en-US).

    Returns:
        InvoiceExtractionResult with extracted fields and confidence scores.
    """
    config = get_azure_ai_client_config()
    if not validate_provider_config("azure_ai_document_intelligence", config):
        raise ValueError("Azure AI Document Intelligence configuration is incomplete. "
                        "Set AZURE_AI_ENDPOINT and AZURE_AI_KEY environment variables.")

    endpoint = config["endpoint"]
    api_key = config["api_key"]
    api_version = config["api_version"]

    # Initialize Azure AI Document Intelligence client
    credential = AzureKeyCredential(api_key)
    client = DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=credential,
        api_version=api_version,
    )

    logger.info(f"Analyzing invoice with Azure AI model: {AZURE_INVOICE_MODEL_ID}")

    # Analyze invoice using the prebuilt-invoice model
    poller = client.begin_analyze_document(
        model_id=AZURE_INVOICE_MODEL_ID,
        body=document_bytes,
        content_type=content_type,
        locale=locale,
    )

    result = poller.result()

    # Extract invoice fields from Azure response
    invoice_data = result.documents[0] if result.documents else {}
    fields = invoice_data.get("fields", {}) if isinstance(invoice_data, dict) else {}

    # Parse vendor information
    vendor_field = fields.get("VendorName")
    vendor = _get_field_value(vendor_field) if vendor_field else ""

    # Parse invoice number
    invoice_number_field = fields.get("InvoiceId")
    invoice_number = _get_field_value(invoice_number_field) if invoice_number_field else ""

    # Parse invoice date
    invoice_date_field = fields.get("InvoiceDate")
    invoice_date = _get_field_value(invoice_date_field) if invoice_date_field else ""

    # Parse total amount
    total_field = fields.get("InvoiceTotal")
    total_amount = _get_field_amount(total_field) if total_field else 0.0

    # Parse currency
    currency_field = fields.get("InvoiceTotal")
    currency = "USD"  # Default currency
    if currency_field and hasattr(currency_field, "value_currency"):
        currency = getattr(currency_field, "value_currency", "USD") or "USD"

    # Parse line items
    line_items = []
    items_field = fields.get("Items")
    if items_field and hasattr(items_field, "value"):
        for item in items_field.value:
            item_fields = item.get("fields", {}) if isinstance(item, dict) else {}
            description = _get_field_value(item_fields.get("Description"))
            quantity = _get_field_amount(item_fields.get("Quantity"))
            unit_price = _get_field_amount(item_fields.get("UnitPrice"))
            total_price = _get_field_amount(item_fields.get("Amount"))

            line_items.append(InvoiceLineItem(
                description=description or "",
                quantity=quantity or 0.0,
                unit_price=unit_price or 0.0,
                total_price=total_price or 0.0,
            ))

    # Build confidence scores
    confidence_scores = []
    for field_name, field_obj in fields.items():
        if field_obj and hasattr(field_obj, "confidence"):
            confidence = getattr(field_obj, "confidence", 0.0)
            confidence_scores.append(ConfidenceScore(
                field_name=field_name,
                score=confidence or 0.0,
            ))

    return InvoiceExtractionResult(
        vendor=vendor,
        invoice_number=invoice_number,
        invoice_date=invoice_date,
        total_amount=total_amount,
        currency=currency,
        line_items=line_items,
        confidence_scores=confidence_scores,
        raw_response={"model_id": AZURE_INVOICE_MODEL_ID, "pages": result.pages} if result else {},
    )


def _get_field_value(field_obj) -> Optional[str]:
    """Extract string value from Azure Document Intelligence field object."""
    if field_obj is None:
        return None
    if hasattr(field_obj, "value"):
        val = field_obj.value
        if hasattr(val, "content"):
            return val.content
        return str(val) if val is not None else None
    return None


def _get_field_amount(field_obj) -> Optional[float]:
    """Extract numeric amount from Azure Document Intelligence field object."""
    if field_obj is None:
        return None
    if hasattr(field_obj, "value"):
        val = field_obj.value
        if val is not None:
            try:
                return float(val)
            except (ValueError, TypeError):
                return None
    return None


def extract_invoice_from_file(
    file_path: str,
    content_type: str = "application/pdf",
) -> InvoiceExtractionResult:
    """
    Extract invoice fields from a local file.

    Args:
        file_path: Path to the invoice file.
        content_type: MIME type of the document.

    Returns:
        InvoiceExtractionResult with extracted fields.
    """
    with open(file_path, "rb") as f:
        document_bytes = f.read()
    return extract_invoice_fields(document_bytes, content_type=content_type)
