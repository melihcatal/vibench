"""
document_field_extraction.py - Extract structured fields from OCR-normalized document text
using Azure Document Intelligence prebuilt invoice model.

Provider: Azure Document Intelligence prebuilt invoice
SDK: azure-ai-documentintelligence
Auth: AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY
"""

import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient


AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.environ.get(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
    "https://your-resource.cognitiveservices.azure.com/"
)
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.environ.get(
    "AZURE_DOCUMENT_INTELLIGENCE_KEY", ""
)


def get_invoice_client():
    """Create and return an Azure DocumentIntelligenceClient for invoice extraction."""
    endpoint = AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
    key = AZURE_DOCUMENT_INTELLIGENCE_KEY
    if not endpoint or not key:
        raise ValueError(
            "Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and "
            "AZURE_DOCUMENT_INTELLIGENCE_KEY environment variables."
        )
    credential = AzureKeyCredential(key)
    return DocumentIntelligenceClient(endpoint=endpoint, credential=credential)


def extract_invoice_fields(file_path: str) -> dict:
    """
    Extract structured invoice fields from a document using Azure Document Intelligence
    prebuilt-invoice model.

    Args:
        file_path: Path to the invoice document (image or PDF).

    Returns:
        dict with structured invoice fields including vendor, customer, items, totals.
    """
    client = get_invoice_client()

    with open(file_path, "rb") as f:
        document_bytes = f.read()

    poller = client.begin_analyze_document(
        model_id="prebuilt-invoice",
        body=document_bytes,
    )
    result = poller.result()

    invoice_fields = {}

    if result.documents:
        doc = result.documents[0]
        fields = doc.fields if hasattr(doc, "fields") and doc.fields else {}

        for field_name, field_value in fields.items():
            value = _extract_field_value(field_value)
            confidence = getattr(field_value, "confidence", 0.0)
            invoice_fields[field_name] = {
                "value": value,
                "confidence": confidence,
            }

        invoice_items = []
        if hasattr(doc, "fields") and doc.fields and "Items" in doc.fields:
            items_field = doc.fields["Items"]
            if hasattr(items_field, "value") and items_field.value:
                for item in items_field.value:
                    item_dict = {}
                    if hasattr(item, "properties") and item.properties:
                        for prop_name, prop_value in item.properties.items():
                            item_dict[prop_name] = _extract_field_value(prop_value)
                    invoice_items.append(item_dict)

        invoice_fields["line_items"] = invoice_items

    page_count = len(result.pages) if result.pages else 0
    invoice_fields["page_count"] = page_count

    return invoice_fields


def extract_invoice_fields_from_bytes(document_bytes: bytes) -> dict:
    """
    Extract structured invoice fields from document bytes.

    Args:
        document_bytes: Raw bytes of the invoice document.

    Returns:
        dict with structured invoice fields.
    """
    client = get_invoice_client()

    poller = client.begin_analyze_document(
        model_id="prebuilt-invoice",
        body=document_bytes,
    )
    result = poller.result()

    invoice_fields = {}

    if result.documents:
        doc = result.documents[0]
        fields = doc.fields if hasattr(doc, "fields") and doc.fields else {}

        for field_name, field_value in fields.items():
            value = _extract_field_value(field_value)
            confidence = getattr(field_value, "confidence", 0.0)
            invoice_fields[field_name] = {
                "value": value,
                "confidence": confidence,
            }

        invoice_items = []
        if hasattr(doc, "fields") and doc.fields and "Items" in doc.fields:
            items_field = doc.fields["Items"]
            if hasattr(items_field, "value") and items_field.value:
                for item in items_field.value:
                    item_dict = {}
                    if hasattr(item, "properties") and item.properties:
                        for prop_name, prop_value in item.properties.items():
                            item_dict[prop_name] = _extract_field_value(prop_value)
                    invoice_items.append(item_dict)

        invoice_fields["line_items"] = invoice_items

    page_count = len(result.pages) if result.pages else 0
    invoice_fields["page_count"] = page_count

    return invoice_fields


def _extract_field_value(field_value):
    """Extract a simple Python value from an Azure Document Intelligence field."""
    if field_value is None:
        return None

    value_type = getattr(field_value, "type", "string")

    if value_type == "currency":
        amount = getattr(field_value, "amount", None)
        currency_code = getattr(field_value, "currency_symbol", "")
        return {"amount": amount, "currency": currency_code}
    elif value_type == "date":
        return getattr(field_value, "value", None)
    elif value_type == "address":
        address_parts = {}
        if hasattr(field_value, "value") and field_value.value:
            for attr in ["house_number", "road", "city", "state", "postal_code", "country"]:
                part = getattr(field_value.value, attr, None)
                if part:
                    address_parts[attr] = str(part)
        return address_parts if address_parts else getattr(field_value, "value", None)
    else:
        val = getattr(field_value, "value", None)
        return str(val) if val is not None else None
