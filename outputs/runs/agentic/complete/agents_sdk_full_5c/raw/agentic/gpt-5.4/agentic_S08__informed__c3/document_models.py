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
    vendor_name: Optional[str] = None
    merchant_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    items: List[LineItem] = field(default_factory=list)
    notes: Optional[str] = None
    confidence: Dict[str, float] = field(default_factory=dict)
    raw_provider_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedExpenseRecord:
    record_type: str
    source_document_type: str
    merchant: Optional[str]
    vendor: Optional[str]
    transaction_date: Optional[str]
    total_amount: Optional[float]
    tax_amount: Optional[float]
    currency: Optional[str]
    line_items: List[Dict[str, Any]]
    notes: Optional[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


REQUIRED_FIELDS_BY_TYPE = {
    "invoice": ["vendor_name", "invoice_date", "total"],
    "receipt": ["merchant_name", "total"],
}


def _clean_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None



def parse_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        cleaned = str(value).replace(",", "").replace("$", "").strip()
        return float(Decimal(cleaned))
    except (InvalidOperation, ValueError):
        return None



def normalize_date(value: Optional[str]) -> Optional[str]:
    value = _clean_text(value)
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            continue
    return value



def line_item_to_dict(item: LineItem) -> Dict[str, Any]:
    return asdict(item)



def normalize_extracted_document(document: ExtractedDocument) -> NormalizedExpenseRecord:
    effective_items = document.line_items or document.items
    return NormalizedExpenseRecord(
        record_type="expense",
        source_document_type=document.document_type,
        merchant=_clean_text(document.merchant_name),
        vendor=_clean_text(document.vendor_name),
        transaction_date=normalize_date(document.invoice_date),
        total_amount=parse_float(document.total),
        tax_amount=parse_float(document.tax),
        currency=_clean_text(document.currency),
        line_items=[line_item_to_dict(item) for item in effective_items],
        notes=_clean_text(document.notes),
        metadata={
            "confidence": document.confidence,
        },
    )
