"""
Local request, response, and normalization helpers for Structured Document Extraction.

Defines data models and utility functions for Azure AI Document Intelligence
extraction results, including invoice and receipt field parsing.

Provider: Azure AI Document Intelligence (Form Recognizer)
SDK: azure-ai-documentintelligence
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from azure.ai.documentintelligence.models import (
    AnalyzeResult,
    DocumentField,
    DocumentLineItem,
)


@dataclass
class ExtractedInvoiceField:
    """Normalized invoice field extracted from Azure Document Intelligence."""
    vendor_name: Optional[str] = None
    vendor_address: Optional[str] = None
    invoice_id: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    sub_total: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    currency: Optional[str] = None
    line_items: list[dict] = field(default_factory=list)
    confidence_scores: dict[str, float] = field(default_factory=dict)


@dataclass
class ExtractedReceiptField:
    """Normalized receipt field extracted from Azure Document Intelligence."""
    merchant_name: Optional[str] = None
    merchant_address: Optional[str] = None
    transaction_date: Optional[str] = None
    transaction_time: Optional[str] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    currency: Optional[str] = None
    items: list[dict] = field(default_factory=list)
    confidence_scores: dict[str, float] = field(default_factory=dict)


@dataclass
class NormalizedExpense:
    """Standard expense record schema for downstream processing."""
    expense_id: str
    document_type: str  # 'invoice' or 'receipt'
    vendor: str
    date: str
    total_amount: float
    currency: str
    tax_amount: float
    line_items: list[dict]
    raw_fields: dict[str, Any]
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)


def parse_invoice_from_azure_result(result: AnalyzeResult) -> ExtractedInvoiceField:
    """
    Parse Azure Document Intelligence prebuilt-invoice results into normalized fields.

    Args:
        result: AnalyzeResult from Azure Document Intelligence analysis.

    Returns:
        ExtractedInvoiceField with populated invoice data.
    """
    extracted = ExtractedInvoiceField()

    if not result.documents:
        return extracted

    doc = result.documents[0]
    fields = doc.fields or {}

    # Extract vendor information
    vendor_field = fields.get("VendorName")
    if vendor_field and vendor_field.value:
        extracted.vendor_name = str(vendor_field.value)
        extracted.confidence_scores["vendor_name"] = vendor_field.confidence or 0.0

    vendor_address_field = fields.get("VendorAddress")
    if vendor_address_field and vendor_address_field.value:
        extracted.vendor_address = str(vendor_address_field.value)
        extracted.confidence_scores["vendor_address"] = vendor_address_field.confidence or 0.0

    # Extract invoice ID
    invoice_id_field = fields.get("InvoiceId")
    if invoice_id_field and invoice_id_field.value:
        extracted.invoice_id = str(invoice_id_field.value)
        extracted.confidence_scores["invoice_id"] = invoice_id_field.confidence or 0.0

    # Extract dates
    invoice_date_field = fields.get("InvoiceDate")
    if invoice_date_field and invoice_date_field.value:
        if isinstance(invoice_date_field.value, datetime):
            extracted.invoice_date = invoice_date_field.value.isoformat()
        else:
            extracted.invoice_date = str(invoice_date_field.value)
        extracted.confidence_scores["invoice_date"] = invoice_date_field.confidence or 0.0

    due_date_field = fields.get("DueDate")
    if due_date_field and due_date_field.value:
        if isinstance(due_date_field.value, datetime):
            extracted.due_date = due_date_field.value.isoformat()
        else:
            extracted.due_date = str(due_date_field.value)
        extracted.confidence_scores["due_date"] = due_date_field.confidence or 0.0

    # Extract monetary fields
    sub_total_field = fields.get("SubTotal")
    if sub_total_field and sub_total_field.value is not None:
        extracted.sub_total = float(sub_total_field.value)
        extracted.confidence_scores["sub_total"] = sub_total_field.confidence or 0.0

    tax_field = fields.get("TotalTax")
    if tax_field and tax_field.value is not None:
        extracted.tax = float(tax_field.value)
        extracted.confidence_scores["tax"] = tax_field.confidence or 0.0

    total_field = fields.get("InvoiceTotal")
    if total_field and total_field.value is not None:
        extracted.total = float(total_field.value)
        extracted.confidence_scores["total"] = total_field.confidence or 0.0

    currency_field = fields.get("Currency")
    if currency_field and currency_field.value:
        extracted.currency = str(currency_field.value)

    # Extract line items
    items_field = fields.get("Items")
    if items_field and items_field.value:
        for item in items_field.value:
            line_item = {}
            if isinstance(item, dict):
                for key, value in item.items():
                    if hasattr(value, 'value'):
                        line_item[key] = value.value
                    else:
                        line_item[key] = value
            extracted.line_items.append(line_item)

    return extracted


def parse_receipt_from_azure_result(result: AnalyzeResult) -> ExtractedReceiptField:
    """
    Parse Azure Document Intelligence prebuilt-receipt results into normalized fields.

    Args:
        result: AnalyzeResult from Azure Document Intelligence analysis.

    Returns:
        ExtractedReceiptField with populated receipt data.
    """
    extracted = ExtractedReceiptField()

    if not result.documents:
        return extracted

    doc = result.documents[0]
    fields = doc.fields or {}

    # Extract merchant information
    merchant_field = fields.get("MerchantName")
    if merchant_field and merchant_field.value:
        extracted.merchant_name = str(merchant_field.value)
        extracted.confidence_scores["merchant_name"] = merchant_field.confidence or 0.0

    merchant_address_field = fields.get("MerchantAddress")
    if merchant_address_field and merchant_address_field.value:
        extracted.merchant_address = str(merchant_address_field.value)
        extracted.confidence_scores["merchant_address"] = merchant_address_field.confidence or 0.0

    # Extract transaction date and time
    transaction_date_field = fields.get("TransactionDate")
    if transaction_date_field and transaction_date_field.value:
        if isinstance(transaction_date_field.value, datetime):
            extracted.transaction_date = transaction_date_field.value.isoformat()
        else:
            extracted.transaction_date = str(transaction_date_field.value)
        extracted.confidence_scores["transaction_date"] = transaction_date_field.confidence or 0.0

    transaction_time_field = fields.get("TransactionTime")
    if transaction_time_field and transaction_time_field.value:
        if isinstance(transaction_time_field.value, datetime):
            extracted.transaction_time = transaction_time_field.value.isoformat()
        else:
            extracted.transaction_time = str(transaction_time_field.value)
        extracted.confidence_scores["transaction_time"] = transaction_time_field.confidence or 0.0

    # Extract monetary fields
    subtotal_field = fields.get("Subtotal")
    if subtotal_field and subtotal_field.value is not None:
        extracted.subtotal = float(subtotal_field.value)
        extracted.confidence_scores["subtotal"] = subtotal_field.confidence or 0.0

    tax_field = fields.get("TotalTax")
    if tax_field and tax_field.value is not None:
        extracted.tax = float(tax_field.value)
        extracted.confidence_scores["tax"] = tax_field.confidence or 0.0

    total_field = fields.get("Total")
    if total_field and total_field.value is not None:
        extracted.total = float(total_field.value)
        extracted.confidence_scores["total"] = total_field.confidence or 0.0

    currency_field = fields.get("Currency")
    if currency_field and currency_field.value:
        extracted.currency = str(currency_field.value)

    # Extract items
    items_field = fields.get("Items")
    if items_field and items_field.value:
        for item in items_field.value:
            receipt_item = {}
            if isinstance(item, dict):
                for key, value in item.items():
                    if hasattr(value, 'value'):
                        receipt_item[key] = value.value
                    else:
                        receipt_item[key] = value
            extracted.items.append(receipt_item)

    return extracted


def validate_field_confidence(
    confidence_scores: dict[str, float],
    required_fields: list[str],
    min_confidence: float = 0.7,
) -> tuple[bool, list[str]]:
    """
    Validate that required fields meet minimum confidence thresholds.

    Args:
        confidence_scores: Mapping of field names to confidence values.
        required_fields: List of field names that must be present.
        min_confidence: Minimum acceptable confidence score.

    Returns:
        Tuple of (is_valid, list_of_issues).
    """
    issues = []

    for field_name in required_fields:
        if field_name not in confidence_scores:
            issues.append(f"Missing field: {field_name}")
        elif confidence_scores[field_name] < min_confidence:
            issues.append(
                f"Low confidence for '{field_name}': "
                f"{confidence_scores[field_name]:.2f} < {min_confidence}"
            )

    return len(issues) == 0, issues
