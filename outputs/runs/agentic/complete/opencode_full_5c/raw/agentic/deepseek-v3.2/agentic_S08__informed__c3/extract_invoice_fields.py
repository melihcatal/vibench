import os
from typing import Dict, List, Optional
from document_client import (
    get_azure_document_intelligence_client,
    create_analyze_request,
)
from document_models import (
    InvoiceExtraction,
    ExtractedField,
    LineItem,
    normalize_azure_field,
    parse_azure_line_items,
)
from azure.ai.documentintelligence.models import AnalyzeResult


def extract_invoice_fields(file_path: str) -> InvoiceExtraction:
    client = get_azure_document_intelligence_client()
    analyze_request = create_analyze_request(file_path, model_id="prebuilt-invoice")

    poller = client.begin_analyze_document(analyze_request)
    result: AnalyzeResult = poller.result()

    vendor_field = None
    date_field = None
    total_field = None
    line_items = []

    for document in result.documents:
        fields = document.get("fields", {})

        vendor_dict = fields.get("VendorName")
        if vendor_dict:
            vendor_field = normalize_azure_field(vendor_dict)

        date_dict = fields.get("InvoiceDate")
        if date_dict:
            date_field = normalize_azure_field(date_dict)

        total_dict = fields.get("InvoiceTotal")
        if total_dict:
            total_field = normalize_azure_field(total_dict)

        items_dict = fields.get("Items")
        if items_dict and isinstance(items_dict, list):
            line_items = parse_azure_line_items(items_dict)

    if not vendor_field:
        vendor_field = ExtractedField(
            name="VendorName", value="Unknown", confidence=0.0
        )
    if not date_field:
        date_field = ExtractedField(name="InvoiceDate", value=None, confidence=0.0)
    if not total_field:
        total_field = ExtractedField(name="InvoiceTotal", value=0.0, confidence=0.0)

    return InvoiceExtraction(
        vendor_name=vendor_field,
        invoice_date=date_field,
        invoice_total=total_field,
        line_items=line_items,
        raw_response=result.as_dict(),
    )


def get_vendor_name(invoice: InvoiceExtraction) -> str:
    return str(invoice.vendor_name.value) if invoice.vendor_name.value else "Unknown"


def get_invoice_date(invoice: InvoiceExtraction) -> Optional[str]:
    return str(invoice.invoice_date.value) if invoice.invoice_date.value else None


def get_invoice_total(invoice: InvoiceExtraction) -> float:
    try:
        return (
            float(invoice.invoice_total.value) if invoice.invoice_total.value else 0.0
        )
    except (ValueError, TypeError):
        return 0.0


def get_line_item_details(invoice: InvoiceExtraction) -> List[Dict[str, Any]]:
    items = []
    for item in invoice.line_items:
        items.append(
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price,
                "confidence": item.confidence,
            }
        )
    return items
