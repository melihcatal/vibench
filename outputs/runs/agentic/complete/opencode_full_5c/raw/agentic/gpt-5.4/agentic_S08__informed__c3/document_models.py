from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class DocumentSource:
    content: bytes
    mime_type: str = "application/pdf"
    filename: Optional[str] = None


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: Optional[float] = None


@dataclass
class ExtractedField:
    value: Any
    confidence: Optional[float] = None


@dataclass
class ExtractedExpense:
    document_type: str
    vendor: Optional[ExtractedField] = None
    merchant: Optional[ExtractedField] = None
    invoice_date: Optional[ExtractedField] = None
    total: Optional[ExtractedField] = None
    tax: Optional[ExtractedField] = None
    currency: Optional[ExtractedField] = None
    line_items: List[LineItem] = field(default_factory=list)
    items: List[LineItem] = field(default_factory=list)
    notes: Optional[ExtractedField] = None
    raw_provider_response: Dict[str, Any] = field(default_factory=dict)


def _safe_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, Decimal):
        return float(value)
    try:
        cleaned = str(value).replace(",", "").strip()
        return float(Decimal(cleaned))
    except (InvalidOperation, ValueError, TypeError):
        return None


def _safe_date(value: Any) -> Optional[str]:
    if not value:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    return text


def extracted_field(
    value: Any, confidence: Optional[float] = None
) -> Optional[ExtractedField]:
    if value is None or value == "":
        return None
    return ExtractedField(value=value, confidence=confidence)


def line_item_from_values(
    description: Any,
    quantity: Any = None,
    unit_price: Any = None,
    amount: Any = None,
    confidence: Optional[float] = None,
) -> LineItem:
    return LineItem(
        description=str(description or "").strip(),
        quantity=_safe_float(quantity),
        unit_price=_safe_float(unit_price),
        amount=_safe_float(amount),
        confidence=confidence,
    )


def expense_to_dict(expense: ExtractedExpense) -> Dict[str, Any]:
    return asdict(expense)


def normalize_expense_record(expense: ExtractedExpense) -> Dict[str, Any]:
    vendor_name = None
    if expense.vendor and expense.vendor.value:
        vendor_name = str(expense.vendor.value)
    elif expense.merchant and expense.merchant.value:
        vendor_name = str(expense.merchant.value)
    total_amount = expense.total.value if expense.total else None
    tax_amount = expense.tax.value if expense.tax else None
    currency = expense.currency.value if expense.currency else None
    normalized_items = expense.line_items or expense.items
    return {
        "record_id": str(uuid.uuid4()),
        "document_type": expense.document_type,
        "vendor_name": vendor_name,
        "document_date": _safe_date(
            expense.invoice_date.value if expense.invoice_date else None
        ),
        "amounts": {
            "total": _safe_float(total_amount),
            "tax": _safe_float(tax_amount),
            "currency": currency,
        },
        "items": [asdict(item) for item in normalized_items],
        "notes": expense.notes.value if expense.notes else None,
        "confidence": {
            "vendor": expense.vendor.confidence
            if expense.vendor
            else (expense.merchant.confidence if expense.merchant else None),
            "date": expense.invoice_date.confidence if expense.invoice_date else None,
            "total": expense.total.confidence if expense.total else None,
            "tax": expense.tax.confidence if expense.tax else None,
        },
        "provider_payload": expense.raw_provider_response,
    }
