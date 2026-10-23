"""
Extract invoice fields using Azure Document Intelligence prebuilt invoice model.

Provider: Azure Document Intelligence prebuilt invoice
SDK: azure-ai-documentintelligence
Auth: AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY
Model: prebuilt-invoice (Azure Document Intelligence)
"""

import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence.models import AnalyzeResult

from document_models import (
    InvoiceExtractionResult,
    LineItem,
)
from document_client import (
    build_azure_di_config,
    normalize_amount,
    normalize_date,
)


def extract_invoice_fields_from_file(
    file_path: str,
    model_id: str = "prebuilt-invoice",
) -> InvoiceExtractionResult:
    """
    Extract vendor, date, total, and line-item fields from an invoice
    using Azure Document Intelligence prebuilt-invoice model.

    Args:
        file_path: Path to the invoice file (PDF, image, etc.)
        model_id: Azure Document Intelligence model ID (default: prebuilt-invoice)

    Returns:
        InvoiceExtractionResult with standardized extracted fields.
    """
    config = build_azure_di_config()
    endpoint = config.credentials["endpoint"]
    key = config.credentials["key"]

    client = DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id=model_id,
            body=f,
            content_type="application/octet-stream",
        )
        result: AnalyzeResult = poller.result()

    return _parse_azure_di_invoice_result(result, model_id)


def extract_invoice_fields_from_bytes(
    file_bytes: bytes,
    content_type: str = "application/pdf",
    model_id: str = "prebuilt-invoice",
) -> InvoiceExtractionResult:
    """
    Extract invoice fields from raw bytes using Azure Document Intelligence.

    Args:
        file_bytes: Raw bytes of the invoice file.
        content_type: MIME type of the file.
        model_id: Azure Document Intelligence model ID.

    Returns:
        InvoiceExtractionResult with extracted fields.
    """
    config = build_azure_di_config()
    endpoint = config.credentials["endpoint"]
    key = config.credentials["key"]

    client = DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    from io import BytesIO

    poller = client.begin_analyze_document(
        model_id=model_id,
        body=BytesIO(file_bytes),
        content_type=content_type,
    )
    result: AnalyzeResult = poller.result()

    return _parse_azure_di_invoice_result(result, model_id)


def extract_invoice_fields_from_url(
    file_url: str,
    model_id: str = "prebuilt-invoice",
) -> InvoiceExtractionResult:
    """
    Extract invoice fields from a publicly accessible URL using Azure Document Intelligence.

    Args:
        file_url: URL to the invoice file.
        model_id: Azure Document Intelligence model ID.

    Returns:
        InvoiceExtractionResult with extracted fields.
    """
    config = build_azure_di_config()
    endpoint = config.credentials["endpoint"]
    key = config.credentials["key"]

    client = DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    poller = client.begin_analyze_document(
        model_id=model_id,
        body={"urlSource": file_url},
    )
    result: AnalyzeResult = poller.result()

    return _parse_azure_di_invoice_result(result, model_id)


def _parse_azure_di_invoice_result(
    result: AnalyzeResult,
    model_id: str,
) -> InvoiceExtractionResult:
    """
    Parse Azure Document Intelligence AnalyzeResult into a standardized InvoiceExtractionResult.
    """
    extraction = InvoiceExtractionResult(
        provider="azure_document_intelligence",
        model_id=model_id,
        raw_response=_serialize_analyze_result(result),
    )

    documents = result.documents if result.documents else []
    if not documents:
        return extraction

    doc = documents[0]
    fields = doc.fields if doc.fields else {}

    # Vendor name
    vendor_field = fields.get("VendorName")
    if vendor_field and vendor_field.value:
        extraction.vendor_name = str(vendor_field.value)
        extraction.vendor_confidence = float(vendor_field.confidence) if vendor_field.confidence else 0.0

    # Invoice ID / number
    invoice_id_field = fields.get("InvoiceId")
    if invoice_id_field and invoice_id_field.value:
        extraction.invoice_number = str(invoice_id_field.value)
        extraction.invoice_number_confidence = (
            float(invoice_id_field.confidence) if invoice_id_field.confidence else 0.0
        )

    # Invoice date
    invoice_date_field = fields.get("InvoiceDate")
    if invoice_date_field and invoice_date_field.value:
        date_val = invoice_date_field.value
        if hasattr(date_val, "strftime"):
            extraction.invoice_date = date_val.strftime("%Y-%m-%d")
        else:
            extraction.invoice_date = normalize_date(str(date_val))
        extraction.invoice_date_confidence = (
            float(invoice_date_field.confidence) if invoice_date_field.confidence else 0.0
        )

    # Invoice total
    total_field = fields.get("InvoiceTotal")
    if total_field and total_field.value is not None:
        extraction.total_amount = float(total_field.value)
        extraction.total_confidence = (
            float(total_field.confidence) if total_field.confidence else 0.0
        )

    # Tax total
    tax_field = fields.get("TotalTax")
    if tax_field and tax_field.value is not None:
        extraction.tax_amount = float(tax_field.value)
        extraction.tax_confidence = (
            float(tax_field.confidence) if tax_field.confidence else 0.0
        )

    # Line items
    items_field = fields.get("Items")
    if items_field and items_field.value:
        for item_data in items_field.value:
            if not isinstance(item_data, dict):
                continue
            line_item = LineItem(
                description=str(item_data.get("Description", "")),
                quantity=float(item_data["Quantity"]) if item_data.get("Quantity") is not None else None,
                unit_price=float(item_data["UnitPrice"]) if item_data.get("UnitPrice") is not None else None,
                total_price=float(item_data["Amount"]) if item_data.get("Amount") is not None else None,
                tax_amount=float(item_data["Tax"]) if item_data.get("Tax") is not None else None,
                confidence=float(item_data.get("confidence", 1.0)),
            )
            extraction.line_items.append(line_item)

    # Vendor address (if needed)
    vendor_addr = fields.get("VendorAddress")
    if vendor_addr and vendor_addr.value:
        if hasattr(vendor_addr.value, "value"):
            addr_val = vendor_addr.value.value
        else:
            addr_val = str(vendor_addr.value)
        if "vendor_address" not in extraction.raw_response:
            extraction.raw_response["vendor_address"] = addr_val

    return extraction


def _serialize_analyze_result(result: AnalyzeResult) -> dict:
    """Serialize an AnalyzeResult to a plain dict for storage."""
    output = {}
    if result.documents:
        doc = result.documents[0]
        output["doc_type"] = doc.doc_type if hasattr(doc, "doc_type") else ""
        output["fields"] = {}
        if doc.fields:
            for field_name, field_val in doc.fields.items():
                if field_val:
                    f_data = {"value": str(field_val.value) if field_val.value else None}
                    if field_val.confidence is not None:
                        f_data["confidence"] = field_val.confidence
                    output["fields"][field_name] = f_data
    return output
