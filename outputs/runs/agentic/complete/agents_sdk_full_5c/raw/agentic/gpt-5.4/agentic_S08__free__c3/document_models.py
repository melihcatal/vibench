from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: Optional[float] = None


@dataclass
class ExtractedDocument:
    document_type: str
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    invoice_date: Optional[str] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    currency: Optional[str] = None
    notes: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    raw_fields: Dict[str, Any] = field(default_factory=dict)
    provider: Optional[str] = None
    model: Optional[str] = None


@dataclass
class NormalizedExpenseRecord:
    source_document_type: str
    supplier_name: Optional[str]
    transaction_date: Optional[str]
    total_amount: Optional[float]
    tax_amount: Optional[float]
    currency: Optional[str]
    memo: Optional[str]
    items: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    field_confidences: Dict[str, float] = field(default_factory=dict)


def to_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        cleaned = str(value).replace(",", "").replace("$", "").strip()
        return float(Decimal(cleaned))
    except (InvalidOperation, ValueError, TypeError):
        return None


def normalize_date(value: Any) -> Optional[str]:
    if not value:
        return None
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    return text


def line_item_to_dict(item: LineItem) -> Dict[str, Any]:
    return asdict(item)


def document_to_dict(doc: ExtractedDocument) -> Dict[str, Any]:
    payload = asdict(doc)
    payload["line_items"] = [line_item_to_dict(item) for item in doc.line_items]
    return payload


def normalized_record_to_dict(record: NormalizedExpenseRecord) -> Dict[str, Any]:
    return asdict(record)


def build_normalized_record(doc: ExtractedDocument) -> NormalizedExpenseRecord:
    supplier_name = doc.vendor or doc.merchant
    transaction_date = normalize_date(doc.invoice_date)
    items = [line_item_to_dict(item) for item in doc.line_items]
    return NormalizedExpenseRecord(
        source_document_type=doc.document_type,
        supplier_name=supplier_name,
        transaction_date=transaction_date,
        total_amount=to_float(doc.total),
        tax_amount=to_float(doc.tax),
        currency=doc.currency,
        memo=doc.notes,
        items=items,
        metadata={
            "provider": doc.provider,
            "model": doc.model,
            "raw_fields": doc.raw_fields,
        },
    )
