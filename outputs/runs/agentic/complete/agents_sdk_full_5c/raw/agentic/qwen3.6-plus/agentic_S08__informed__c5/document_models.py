"""
Local request, response, and normalization helpers for Structured Document Extraction.
Defines data models, schema validators, and normalization utilities.
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class DocumentType(str, Enum):
    INVOICE = "invoice"
    RECEIPT = "receipt"


@dataclass
class LineItem:
    """Represents a single line item from an invoice or receipt."""
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    product_code: Optional[str] = None
    tax_rate: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class InvoiceFields:
    """Standardized invoice extraction result."""
    vendor_name: Optional[str] = None
    vendor_address: Optional[str] = None
    invoice_date: Optional[str] = None
    invoice_number: Optional[str] = None
    total_amount: Optional[float] = None
    total_net: Optional[float] = None
    total_tax: Optional[float] = None
    currency: Optional[str] = None
    confidence: Optional[float] = None
    line_items: List[LineItem] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["line_items"] = [li.to_dict() for li in self.line_items if li]
        return {k: v for k, v in result.items() if v is not None and v != [] and v != [{}]}


@dataclass
class ReceiptFields:
    """Standardized receipt extraction result."""
    merchant_name: Optional[str] = None
    receipt_date: Optional[str] = None
    receipt_time: Optional[str] = None
    total_amount: Optional[float] = None
    total_tax: Optional[float] = None
    subtotal: Optional[float] = None
    currency: Optional[str] = None
    payment_method: Optional[str] = None
    confidence: Optional[float] = None
    items: List[LineItem] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["items"] = [li.to_dict() for li in self.items if li]
        return {k: v for k, v in result.items() if v is not None and v != [] and v != [{}]}


@dataclass
class NormalizedExpense:
    """
    Unified expense record normalized from either an invoice or receipt.
    Conforms to a standard JSON schema for downstream consumption.
    """
    expense_id: str
    document_type: DocumentType
    source_vendor: Optional[str] = None
    expense_date: Optional[str] = None
    document_reference: Optional[str] = None
    currency: Optional[str] = None
    subtotal: Optional[float] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    payment_method: Optional[str] = None
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    confidence: Optional[float] = None
    raw_fields: Optional[Dict[str, Any]] = None
    normalized_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, default=str)


def normalize_invoice_to_expense(
    invoice_fields: Dict[str, Any],
    expense_id: str,
) -> NormalizedExpense:
    """
    Normalize extracted invoice fields into a standard NormalizedExpense record.

    Args:
        invoice_fields: Dictionary of extracted invoice fields from Mindee.
        expense_id: Unique identifier for the expense record.

    Returns:
        NormalizedExpense dataclass instance.
    """
    line_items = []
    for item in invoice_fields.get("line_items", []):
        line_items.append({
            "description": item.get("description"),
            "quantity": item.get("quantity"),
            "unit_price": item.get("unit_price"),
            "total_amount": item.get("total_amount"),
            "tax_amount": item.get("tax_amount"),
        })

    return NormalizedExpense(
        expense_id=expense_id,
        document_type=DocumentType.INVOICE,
        source_vendor=invoice_fields.get("vendor_name"),
        expense_date=invoice_fields.get("invoice_date"),
        document_reference=invoice_fields.get("invoice_number"),
        currency=invoice_fields.get("currency"),
        subtotal=invoice_fields.get("total_net"),
        tax_amount=invoice_fields.get("total_tax"),
        total_amount=invoice_fields.get("total_amount"),
        line_items=line_items,
        confidence=invoice_fields.get("confidence"),
        raw_fields=invoice_fields,
        normalized_at=datetime.utcnow().isoformat(),
    )


def normalize_receipt_to_expense(
    receipt_fields: Dict[str, Any],
    expense_id: str,
) -> NormalizedExpense:
    """
    Normalize extracted receipt fields into a standard NormalizedExpense record.

    Args:
        receipt_fields: Dictionary of extracted receipt fields from Mindee.
        expense_id: Unique identifier for the expense record.

    Returns:
        NormalizedExpense dataclass instance.
    """
    items = []
    for item in receipt_fields.get("items", []):
        items.append({
            "description": item.get("description"),
            "quantity": item.get("quantity"),
            "unit_price": item.get("unit_price"),
            "total_amount": item.get("total_amount"),
            "tax_rate": item.get("tax_rate"),
        })

    return NormalizedExpense(
        expense_id=expense_id,
        document_type=DocumentType.RECEIPT,
        source_vendor=receipt_fields.get("merchant_name"),
        expense_date=receipt_fields.get("receipt_date"),
        document_reference=None,
        currency=receipt_fields.get("currency"),
        subtotal=receipt_fields.get("subtotal"),
        tax_amount=receipt_fields.get("total_tax"),
        total_amount=receipt_fields.get("total_amount"),
        payment_method=receipt_fields.get("payment_method"),
        line_items=items,
        confidence=receipt_fields.get("confidence"),
        raw_fields=receipt_fields,
        normalized_at=datetime.utcnow().isoformat(),
    )


def validate_required_fields(
    fields: Dict[str, Any],
    required_keys: List[str],
    min_confidence: float = 0.5,
) -> Dict[str, Any]:
    """
    Validate that required fields are present and meet confidence thresholds.

    Args:
        fields: Dictionary of extracted fields with confidence scores.
        required_keys: List of required field names.
        min_confidence: Minimum acceptable confidence score (0.0-1.0).

    Returns:
        Validation result dictionary with 'valid', 'missing_fields',
        'low_confidence_fields', and 'errors'.
    """
    missing_fields = []
    low_confidence_fields = []
    errors = []

    doc_confidence = fields.get("confidence", 0.0)

    if doc_confidence is not None and doc_confidence < min_confidence:
        errors.append(
            f"Document confidence {doc_confidence:.2f} "
            f"is below minimum threshold {min_confidence:.2f}"
        )

    for key in required_keys:
        value = fields.get(key)
        if value is None or (isinstance(value, str) and value.strip() == ""):
            missing_fields.append(key)
        elif key == "total_amount" and value is None:
            missing_fields.append(key)

    if missing_fields:
        errors.append(f"Missing required fields: {', '.join(missing_fields)}")

    return {
        "valid": len(errors) == 0,
        "missing_fields": missing_fields,
        "low_confidence_fields": low_confidence_fields,
        "errors": errors,
        "document_confidence": doc_confidence,
    }


def validate_confidence_scores(
    fields: Dict[str, Any],
    min_field_confidence: float = 0.5,
) -> Dict[str, Any]:
    """
    Check confidence scores on individual extracted fields.

    Args:
        fields: Dictionary of extracted fields.
        min_field_confidence: Minimum acceptable per-field confidence.

    Returns:
        Validation result with fields below confidence threshold flagged.
    """
    low_confidence_fields = []
    doc_confidence = fields.get("confidence")

    if doc_confidence is not None and doc_confidence < min_field_confidence:
        low_confidence_fields.append({
            "field": "document",
            "confidence": doc_confidence,
            "threshold": min_field_confidence,
        })

    return {
        "low_confidence_fields": low_confidence_fields,
        "document_confidence": doc_confidence,
        "passes_threshold": doc_confidence is None or doc_confidence >= min_field_confidence,
    }
