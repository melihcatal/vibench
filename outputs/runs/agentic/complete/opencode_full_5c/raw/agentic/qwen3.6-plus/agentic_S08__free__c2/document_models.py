import os
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from datetime import datetime


@dataclass
class LineItem:
    description: str
    quantity: float
    unit_price: float
    total: float
    confidence: float = 1.0


@dataclass
class InvoiceFields:
    vendor: str
    invoice_date: str
    total_amount: float
    line_items: list[LineItem] = field(default_factory=list)
    currency: str = "USD"
    invoice_number: str = ""
    confidence: float = 1.0
    raw_text: str = ""


@dataclass
class ReceiptFields:
    merchant: str
    receipt_date: str
    total_amount: float
    tax_amount: float = 0.0
    items: list[LineItem] = field(default_factory=list)
    currency: str = "USD"
    confidence: float = 1.0
    raw_text: str = ""


@dataclass
class ExpenseRecord:
    document_type: str
    vendor_or_merchant: str
    date: str
    total_amount: float
    tax_amount: float = 0.0
    currency: str = "USD"
    line_items: list[dict] = field(default_factory=list)
    confidence: float = 1.0
    source_provider: str = ""
    normalized_at: str = ""
    record_id: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class FieldValidationResult:
    field_name: str
    present: bool
    valid: bool
    confidence: float
    issues: list[str] = field(default_factory=list)


@dataclass
class DocumentValidationResult:
    document_type: str
    overall_valid: bool
    field_results: list[FieldValidationResult]
    overall_confidence: float = 0.0
    validation_timestamp: str = ""


@dataclass
class InvoiceSummary:
    vendor: str
    invoice_date: str
    total_amount: float
    line_item_count: int
    average_item_price: float
    currency: str
    summary_text: str = ""


@dataclass
class ModerationResult:
    text: str
    flagged: bool
    categories: dict[str, bool] = field(default_factory=dict)
    category_scores: dict[str, float] = field(default_factory=dict)
    provider: str = ""


@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str = ""
    target_language: str = ""
    provider: str = ""


REQUIRED_INVOICE_FIELDS = ["vendor", "invoice_date", "total_amount", "line_items"]
REQUIRED_RECEIPT_FIELDS = ["merchant", "receipt_date", "total_amount", "tax_amount"]
REQUIRED_EXPENSE_FIELDS = [
    "document_type",
    "vendor_or_merchant",
    "date",
    "total_amount",
]

MINIMUM_CONFIDENCE_THRESHOLD = 0.75

STANDARD_EXPENSE_SCHEMA = {
    "document_type": "string",
    "vendor_or_merchant": "string",
    "date": "string (ISO 8601)",
    "total_amount": "number",
    "tax_amount": "number",
    "currency": "string (ISO 4217)",
    "line_items": "array",
    "confidence": "number",
    "normalized_at": "string (ISO 8601)",
    "record_id": "string",
}


def invoice_fields_to_expense_record(
    invoice: InvoiceFields, source_provider: str = ""
) -> ExpenseRecord:
    return ExpenseRecord(
        document_type="invoice",
        vendor_or_merchant=invoice.vendor,
        date=invoice.invoice_date,
        total_amount=invoice.total_amount,
        currency=invoice.currency,
        line_items=[asdict(item) for item in invoice.line_items],
        confidence=invoice.confidence,
        source_provider=source_provider,
        normalized_at=datetime.utcnow().isoformat(),
    )


def receipt_fields_to_expense_record(
    receipt: ReceiptFields, source_provider: str = ""
) -> ExpenseRecord:
    return ExpenseRecord(
        document_type="receipt",
        vendor_or_merchant=receipt.merchant,
        date=receipt.receipt_date,
        total_amount=receipt.total_amount,
        tax_amount=receipt.tax_amount,
        currency=receipt.currency,
        line_items=[asdict(item) for item in receipt.items],
        confidence=receipt.confidence,
        source_provider=source_provider,
        normalized_at=datetime.utcnow().isoformat(),
    )


def expense_record_to_dict(record: ExpenseRecord) -> dict[str, Any]:
    return asdict(record)


def dict_to_expense_record(data: dict[str, Any]) -> ExpenseRecord:
    return ExpenseRecord(**data)
