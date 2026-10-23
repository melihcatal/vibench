import os
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ExtractedField:
    value: Any
    confidence: float = 0.0
    page_number: Optional[int] = None


@dataclass
class LineItem:
    description: ExtractedField = field(
        default_factory=lambda: ExtractedField(value="")
    )
    quantity: ExtractedField = field(default_factory=lambda: ExtractedField(value=0))
    unit_price: ExtractedField = field(
        default_factory=lambda: ExtractedField(value=0.0)
    )
    total_price: ExtractedField = field(
        default_factory=lambda: ExtractedField(value=0.0)
    )


@dataclass
class InvoiceExtraction:
    vendor_name: ExtractedField = field(
        default_factory=lambda: ExtractedField(value="")
    )
    invoice_date: ExtractedField = field(
        default_factory=lambda: ExtractedField(value="")
    )
    invoice_total: ExtractedField = field(
        default_factory=lambda: ExtractedField(value=0.0)
    )
    line_items: list[LineItem] = field(default_factory=list)
    raw_response: Optional[dict] = None


@dataclass
class ReceiptItem:
    description: ExtractedField = field(
        default_factory=lambda: ExtractedField(value="")
    )
    price: ExtractedField = field(default_factory=lambda: ExtractedField(value=0.0))


@dataclass
class ReceiptExtraction:
    merchant_name: ExtractedField = field(
        default_factory=lambda: ExtractedField(value="")
    )
    tax_amount: ExtractedField = field(
        default_factory=lambda: ExtractedField(value=0.0)
    )
    receipt_total: ExtractedField = field(
        default_factory=lambda: ExtractedField(value=0.0)
    )
    items: list[ReceiptItem] = field(default_factory=list)
    raw_response: Optional[dict] = None


@dataclass
class NormalizedExpense:
    document_type: str = ""
    vendor_or_merchant: str = ""
    document_date: str = ""
    subtotal: float = 0.0
    tax: float = 0.0
    total: float = 0.0
    line_items: list[dict] = field(default_factory=list)
    currency: str = "USD"
    source_document_id: str = ""
    extraction_confidence: float = 0.0

    def to_dict(self) -> dict:
        return {
            "document_type": self.document_type,
            "vendor_or_merchant": self.vendor_or_merchant,
            "document_date": self.document_date,
            "subtotal": self.subtotal,
            "tax": self.tax,
            "total": self.total,
            "line_items": self.line_items,
            "currency": self.currency,
            "source_document_id": self.source_document_id,
            "extraction_confidence": self.extraction_confidence,
        }


@dataclass
class ValidationResult:
    is_valid: bool
    missing_fields: list[str] = field(default_factory=list)
    low_confidence_fields: list[str] = field(default_factory=list)
    confidence_threshold: float = 0.5
    details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "is_valid": self.is_valid,
            "missing_fields": self.missing_fields,
            "low_confidence_fields": self.low_confidence_fields,
            "confidence_threshold": self.confidence_threshold,
            "details": self.details,
        }


@dataclass
class DocumentExtractionRequest:
    file_path: Optional[str] = None
    file_bytes: Optional[bytes] = None
    content_type: str = "application/pdf"
    locale: str = "en-US"
