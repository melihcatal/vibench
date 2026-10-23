"""
Extract merchant, tax, total, and items from a receipt document.

Uses Azure AI Document Intelligence prebuilt-receipt model to analyze
receipt documents and extract structured fields.

Provider: Azure AI Document Intelligence (Form Recognizer)
Model: prebuilt-receipt
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
    ExtractedReceiptField,
    parse_receipt_from_azure_result,
)


def extract_receipt_fields(
    file_path: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ExtractedReceiptField:
    """
    Extract structured fields from a receipt document using Azure AI Document Intelligence.

    Extracts:
        - merchant_name: Merchant/store name
        - merchant_address: Merchant address
        - transaction_date: Date of transaction
        - transaction_time: Time of transaction
        - subtotal: Pre-tax subtotal
        - tax: Total tax amount
        - total: Receipt total
        - currency: Currency code
        - items: List of purchased items

    Args:
        file_path: Path to the receipt document (PDF, PNG, JPEG, TIFF, BMP).
        endpoint: Azure Document Intelligence endpoint URL.
                  Falls back to AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT env var.
        api_key: Azure Document Intelligence API key.
                 Falls back to AZURE_DOCUMENT_INTELLIGENCE_KEY env var.

    Returns:
        ExtractedReceiptField containing all extracted receipt fields and confidence scores.

    Raises:
        ValueError: If credentials are not provided.
        Exception: If the Azure API call fails.
    """
    client, model_id = get_analysis_client_for_prebuilt(
        model_id="prebuilt-receipt",
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

    extracted = parse_receipt_from_azure_result(result)

    return extracted


def extract_receipt_fields_from_bytes(
    file_bytes: bytes,
    content_type: str = "image/jpeg",
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ExtractedReceiptField:
    """
    Extract structured fields from receipt document bytes using Azure AI Document Intelligence.

    Args:
        file_bytes: Raw bytes of the receipt document.
        content_type: MIME type of the document.
        endpoint: Azure Document Intelligence endpoint URL.
        api_key: Azure Document Intelligence API key.

    Returns:
        ExtractedReceiptField containing all extracted receipt fields.
    """
    client, model_id = get_analysis_client_for_prebuilt(
        model_id="prebuilt-receipt",
        endpoint=endpoint,
        api_key=api_key,
    )

    poller = client.begin_analyze_document(
        model_id=model_id,
        analyze_request=file_bytes,
        content_type=content_type,
    )

    result: AnalyzeResult = poller.result()

    return parse_receipt_from_azure_result(result)


def format_receipt_output(extracted: ExtractedReceiptField) -> dict:
    """
    Format extracted receipt fields into a structured output dictionary.

    Args:
        extracted: ExtractedReceiptField from Azure analysis.

    Returns:
        Dictionary with formatted receipt data.
    """
    return {
        "merchant": {
            "name": extracted.merchant_name,
            "address": extracted.merchant_address,
        },
        "transaction": {
            "date": extracted.transaction_date,
            "time": extracted.transaction_time,
        },
        "financials": {
            "subtotal": extracted.subtotal,
            "tax": extracted.tax,
            "total": extracted.total,
            "currency": extracted.currency,
        },
        "items": extracted.items,
        "confidence_scores": extracted.confidence_scores,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_receipt_fields.py <receipt_file_path>")
        sys.exit(1)

    receipt_path = sys.argv[1]
    if not os.path.exists(receipt_path):
        print(f"File not found: {receipt_path}")
        sys.exit(1)

    result = extract_receipt_fields(receipt_path)
    output = format_receipt_output(result)
    print(output)
