import os
import json
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class LineItem:
    description: str
    quantity: float
    unit_price: float
    total: float


@dataclass
class InvoiceExtraction:
    vendor_name: str = ""
    invoice_date: str = ""
    invoice_number: str = ""
    total_amount: float = 0.0
    tax_amount: float = 0.0
    currency: str = "USD"
    line_items: List[LineItem] = field(default_factory=list)
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class ReceiptExtraction:
    merchant_name: str = ""
    receipt_date: str = ""
    total_amount: float = 0.0
    tax_amount: float = 0.0
    payment_method: str = ""
    items: List[Dict[str, Any]] = field(default_factory=list)
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class NormalizedExpense:
    document_type: str = ""
    vendor: str = ""
    date: str = ""
    total: float = 0.0
    tax: float = 0.0
    currency: str = "USD"
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    source_document_id: str = ""
    normalized_at: str = ""
    schema_version: str = "1.0"


@dataclass
class DocumentValidationResult:
    is_valid: bool = False
    missing_fields: List[str] = field(default_factory=list)
    low_confidence_fields: List[str] = field(default_factory=list)
    confidence_threshold: float = 0.7
    validation_details: Dict[str, Any] = field(default_factory=dict)


def normalize_invoice_to_expense(
    invoice: InvoiceExtraction, document_id: str
) -> NormalizedExpense:
    return NormalizedExpense(
        document_type="invoice",
        vendor=invoice.vendor_name,
        date=invoice.invoice_date,
        total=invoice.total_amount,
        tax=invoice.tax_amount,
        currency=invoice.currency,
        line_items=[asdict(item) for item in invoice.line_items],
        source_document_id=document_id,
        normalized_at=datetime.utcnow().isoformat(),
        schema_version="1.0",
    )


def normalize_receipt_to_expense(
    receipt: ReceiptExtraction, document_id: str
) -> NormalizedExpense:
    return NormalizedExpense(
        document_type="receipt",
        vendor=receipt.merchant_name,
        date=receipt.receipt_date,
        total=receipt.total_amount,
        tax=receipt.tax_amount,
        currency="USD",
        line_items=receipt.items,
        source_document_id=document_id,
        normalized_at=datetime.utcnow().isoformat(),
        schema_version="1.0",
    )


def build_expense_schema() -> Dict[str, Any]:
    return {
        "type": "object",
        "required": [
            "document_type",
            "vendor",
            "date",
            "total",
            "currency",
            "source_document_id",
            "normalized_at",
            "schema_version",
        ],
        "properties": {
            "document_type": {"type": "string", "enum": ["invoice", "receipt"]},
            "vendor": {"type": "string", "minLength": 1},
            "date": {"type": "string", "format": "date"},
            "total": {"type": "number", "minimum": 0},
            "tax": {"type": "number", "minimum": 0},
            "currency": {"type": "string", "pattern": "^[A-Z]{3}$"},
            "line_items": {"type": "array", "items": {"type": "object"}},
            "source_document_id": {"type": "string"},
            "normalized_at": {"type": "string", "format": "date-time"},
            "schema_version": {"type": "string", "pattern": "^\\d+\\.\\d+$"},
        },
    }
