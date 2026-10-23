from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class DocumentSource:
    content: bytes
    filename: str | None = None
    mime_type: str = "application/pdf"


@dataclass
class LineItem:
    description: str | None = None
    quantity: float | None = None
    unit_price: float | None = None
    amount: float | None = None
    tax: float | None = None
    confidence: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ExtractedField:
    value: Any
    confidence: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class InvoiceExtraction:
    vendor: ExtractedField | None = None
    invoice_date: ExtractedField | None = None
    total: ExtractedField | None = None
    line_items: list[LineItem] = field(default_factory=list)
    raw_response: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "vendor": self.vendor.to_dict() if self.vendor else None,
            "invoice_date": self.invoice_date.to_dict() if self.invoice_date else None,
            "total": self.total.to_dict() if self.total else None,
            "line_items": [item.to_dict() for item in self.line_items],
            "raw_response": self.raw_response,
        }


@dataclass
class ReceiptExtraction:
    merchant: ExtractedField | None = None
    tax: ExtractedField | None = None
    total: ExtractedField | None = None
    items: list[LineItem] = field(default_factory=list)
    raw_response: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "merchant": self.merchant.to_dict() if self.merchant else None,
            "tax": self.tax.to_dict() if self.tax else None,
            "total": self.total.to_dict() if self.total else None,
            "items": [item.to_dict() for item in self.items],
            "raw_response": self.raw_response,
        }


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        cleaned = str(value).replace(",", "").strip()
        return float(cleaned)
    except (TypeError, ValueError):
        return None


def normalize_date(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    text = str(value).strip()
    if not text:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    return text


def average_confidence(values: list[float | None]) -> float | None:
    filtered = [v for v in values if v is not None]
    if not filtered:
        return None
    return sum(filtered) / len(filtered)


def build_expense_record(
    document_type: str,
    supplier_name: str | None,
    document_date: str | None,
    total_amount: float | None,
    tax_amount: float | None,
    currency: str | None,
    line_items: list[dict[str, Any]],
    source_payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "document_type": document_type,
        "supplier_name": supplier_name,
        "document_date": document_date,
        "total_amount": total_amount,
        "tax_amount": tax_amount,
        "currency": currency,
        "line_items": line_items,
        "source_payload": source_payload,
    }
