"""
Extract vendor, date, total, and line-item fields from an invoice document.

Uses Azure AI Document Intelligence prebuilt-invoice model to analyze
invoice documents and extract structured fields.

Provider: Azure AI Document Intelligence (Form Recognizer)
Model: prebuilt-invoice
SDK: azure-ai-documentintelligence
Endpoint: https://{resource-name}.cognitiveservices.azure.com
"""

import os
import sys
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult

from document_client import (
    get_document_client,
    build_analysis_request,
    get_analysis_client_for_prebuilt,
)
from document_models import (
    ExtractedInvoiceField,
    parse_invoice_from_azure_result,
)


def extract_invoice_fields(
    file_path: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ExtractedInvoiceField:
    """
    Extract structured fields from an invoice document using Azure AI Document Intelligence.

    Extracts:
        - vendor_name: Vendor/merchant name
        - vendor_address: Vendor address
        - invoice_id: Invoice number/identifier
        - invoice_date: Invoice date
        - due_date: Payment due date
        - sub_total: Pre-tax subtotal
        - tax: Total tax amount
        - total: Invoice total
        - currency: Currency code
        - line_items: List of line item details

    Args:
        file_path: Path to the invoice document (PDF, PNG, JPEG, TIFF, BMP).
        endpoint: Azure Document Intelligence endpoint URL.
                  Falls back to AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT env var.
        api_key: Azure Document Intelligence API key.
                 Falls back to AZURE_DOCUMENT_INTELLIGENCE_KEY env var.

    Returns:
        ExtractedInvoiceField containing all extracted invoice fields and confidence scores.

    Raises:
        ValueError: If credentials are not provided.
        Exception: If the Azure API call fails.
    """
    client, model_id = get_analysis_client_for_prebuilt(
        model_id="prebuilt-invoice",
        endpoint=endpoint,
        api_key=api_key,
    )

    file_bytes, content_type = build_analysis_request(file_path)

    poller = client.begin_analyze_document(
        model_id=model_id,
        analyze_request=file_bytes,
        content_type=content_type,
    )

    result: AnalyzeResult = poller.result()

    extracted = parse_invoice_from_azure_result(result)

    return extracted


def extract_invoice_fields_from_bytes(
    file_bytes: bytes,
    content_type: str = "application/pdf",
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ExtractedInvoiceField:
    """
    Extract structured fields from invoice document bytes using Azure AI Document Intelligence.

    Args:
        file_bytes: Raw bytes of the invoice document.
        content_type: MIME type of the document.
        endpoint: Azure Document Intelligence endpoint URL.
        api_key: Azure Document Intelligence API key.

    Returns:
        ExtractedInvoiceField containing all extracted invoice fields.
    """
    client, model_id = get_analysis_client_for_prebuilt(
        model_id="prebuilt-invoice",
        endpoint=endpoint,
        api_key=api_key,
    )

    poller = client.begin_analyze_document(
        model_id=model_id,
        analyze_request=file_bytes,
        content_type=content_type,
    )

    result: AnalyzeResult = poller.result()

    return parse_invoice_from_azure_result(result)


def format_invoice_output(extracted: ExtractedInvoiceField) -> dict:
    """
    Format extracted invoice fields into a structured output dictionary.

    Args:
        extracted: ExtractedInvoiceField from Azure analysis.

    Returns:
        Dictionary with formatted invoice data.
    """
    return {
        "vendor": {
            "name": extracted.vendor_name,
            "address": extracted.vendor_address,
        },
        "invoice_details": {
            "invoice_id": extracted.invoice_id,
            "invoice_date": extracted.invoice_date,
            "due_date": extracted.due_date,
        },
        "financials": {
            "sub_total": extracted.sub_total,
            "tax": extracted.tax,
            "total": extracted.total,
            "currency": extracted.currency,
        },
        "line_items": extracted.line_items,
        "confidence_scores": extracted.confidence_scores,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_invoice_fields.py <invoice_file_path>")
        sys.exit(1)

    invoice_path = sys.argv[1]
    if not os.path.exists(invoice_path):
        print(f"File not found: {invoice_path}")
        sys.exit(1)

    result = extract_invoice_fields(invoice_path)
    output = format_invoice_output(result)
    print(output)
