"""
Extracts structured fields from OCR-normalized document text using Mindee Invoice OCR.
Uses the Mindee Python SDK with the prebuilt invoice processor for field extraction.
"""

import os
from typing import Dict, List, Optional, Any

from mindee import Client
from mindee.input import InputSource
from mindee.client import PageOptions
from mindee.parsing.standard import AmountField, DateField, StringField, LocaleField

from document_models import DocumentTextResult


def get_mindee_api_key() -> str:
    """Retrieve Mindee API key from environment."""
    key = os.environ.get("MINDEE_API_KEY")
    if not key:
        raise ValueError("MINDEE_API_KEY environment variable is required")
    return key


def create_mindee_client() -> Client:
    """
    Create and return an authenticated Mindee client.

    Returns:
        Client: Mindee API client for document processing.
    """
    api_key = get_mindee_api_key()
    return Client(api_key=api_key)


def extract_invoice_fields_from_file(
    file_path: str,
    cutoff: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Extract structured invoice fields from a document file using Mindee Invoice OCR.

    Uses the Mindee prebuilt invoice model (invoice v4) for field extraction.

    Args:
        file_path: Path to the document image or PDF.
        cutoff: Optional page cutoff for multi-page documents.

    Returns:
        Dict[str, Any]: Dictionary with extracted invoice fields including
            total_amount, date, supplier_name, invoice_number, tax_rate, etc.
    """
    client = create_mindee_client()

    input_doc = client.source_from_path(file_path, cut_pdf=cutoff)
    response = client.parse(
        client.product.invoice,
        input_doc,
        page_options=PageOptions(range(cutoff), on_min_pages=0) if cutoff else None,
    )

    invoice = response.document.inference.prediction
    return _parse_invoice_fields(invoice)


def extract_invoice_fields_from_bytes(
    file_bytes: bytes,
    filename: str = "document.pdf",
) -> Dict[str, Any]:
    """
    Extract structured invoice fields from document bytes using Mindee Invoice OCR.

    Args:
        file_bytes: Raw bytes of the document file.
        filename: Name for the file (used to determine file type).

    Returns:
        Dict[str, Any]: Dictionary with extracted invoice fields.
    """
    client = create_mindee_client()
    input_doc = client.source_from_bytes(file_bytes, filename)
    response = client.parse(client.product.invoice, input_doc)

    invoice = response.document.inference.prediction
    return _parse_invoice_fields(invoice)


def _parse_invoice_fields(invoice) -> Dict[str, Any]:
    """
    Parse Mindee invoice prediction into a structured dictionary.

    Args:
        invoice: Mindee InvoicePrediction object.

    Returns:
        Dict[str, Any]: Structured dictionary of extracted fields.
    """
    fields = {}

    # Total amounts
    total_amount = _get_field_value(invoice.total_amount)
    if total_amount is not None:
        fields["total_amount"] = float(total_amount)

    net_amount = _get_field_value(invoice.total_net)
    if net_amount is not None:
        fields["total_net"] = float(net_amount)

    tax_amount = _get_field_value(invoice.total_tax)
    if tax_amount is not None:
        fields["total_tax"] = float(tax_amount)

    # Dates
    date_value = _get_field_value(invoice.date)
    if date_value is not None:
        fields["date"] = str(date_value)

    due_date = _get_field_value(invoice.due_date)
    if due_date is not None:
        fields["due_date"] = str(due_date)

    # Supplier info
    supplier_name = _get_field_value(invoice.supplier_name)
    if supplier_name is not None:
        fields["supplier_name"] = str(supplier_name)

    supplier_address = _get_field_value(invoice.supplier_address)
    if supplier_address is not None:
        fields["supplier_address"] = str(supplier_address)

    supplier_company_reg = _get_field_value(invoice.supplier_company_registrations)
    if supplier_company_reg is not None:
        fields["supplier_company_registrations"] = str(supplier_company_reg)

    # Invoice number
    invoice_number = _get_field_value(invoice.invoice_number)
    if invoice_number is not None:
        fields["invoice_number"] = str(invoice_number)

    # Tax details
    taxes = []
    for tax in invoice.taxes:
        tax_entry = {
            "rate": _get_field_value(tax.rate),
            "amount": _get_field_value(tax.amount),
            "code": _get_field_value(tax.code),
        }
        taxes.append({k: v for k, v in tax_entry.items() if v is not None})
    if taxes:
        fields["taxes"] = taxes

    # Line items
    line_items = []
    for item in invoice.line_items:
        line_entry = {
            "description": _get_field_value(item.description),
            "quantity": _get_field_value(item.quantity),
            "unit_price": _get_field_value(item.unit_price),
            "total_amount": _get_field_value(item.total_amount),
            "tax_rate": _get_field_value(item.tax_rate),
        }
        line_items.append({k: v for k, v in line_entry.items() if v is not None})
    if line_items:
        fields["line_items"] = line_items

    # Locale
    locale = invoice.locale
    if locale:
        fields["locale"] = {
            "language": _get_field_value(locale.language),
            "country": _get_field_value(locale.country),
            "currency": _get_field_value(locale.currency),
        }

    return fields


def _get_field_value(field) -> Optional[Any]:
    """Safely extract the value from a Mindee field object."""
    if field is None:
        return None
    if hasattr(field, "value"):
        return field.value
    return str(field) if field else None


def extract_custom_fields_from_ocr_text(
    ocr_result: DocumentTextResult,
    field_patterns: Dict[str, str],
) -> Dict[str, str]:
    """
    Extract custom structured fields from OCR text using regex patterns.

    Args:
        ocr_result: The DocumentTextResult from OCR extraction.
        field_patterns: Dictionary mapping field names to regex patterns.

    Returns:
        Dict[str, str]: Extracted field values.
    """
    import re

    extracted = {}
    full_text = ocr_result.full_text

    for field_name, pattern in field_patterns.items():
        match = re.search(pattern, full_text, re.IGNORECASE | re.MULTILINE)
        if match:
            extracted[field_name] = match.group(1) if match.groups() else match.group(0)

    return extracted
