from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional


def _to_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = str(value).replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


def _to_confidence(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return default
    if numeric > 1.0:
        numeric = numeric / 100.0
    return max(0.0, min(1.0, numeric))


def _normalize_date(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    raw = value.strip()
    for fmt in (
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%m-%d-%Y",
    ):
        try:
            return datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return raw


@dataclass
class FieldValue:
    value: Any = None
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {"value": self.value, "confidence": _to_confidence(self.confidence)}


@dataclass
class LineItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "quantity": _to_float(self.quantity),
            "unit_price": _to_float(self.unit_price),
            "amount": _to_float(self.amount),
            "confidence": _to_confidence(self.confidence),
        }


@dataclass
class ExtractedDocument:
    document_type: str
    source_provider: str
    source_model: str
    vendor: Optional[FieldValue] = None
    merchant: Optional[FieldValue] = None
    date: Optional[FieldValue] = None
    tax: Optional[FieldValue] = None
    total: Optional[FieldValue] = None
    items: List[LineItem] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_type": self.document_type,
            "source_provider": self.source_provider,
            "source_model": self.source_model,
            "vendor": self.vendor.to_dict() if self.vendor else None,
            "merchant": self.merchant.to_dict() if self.merchant else None,
            "date": self.date.to_dict() if self.date else None,
            "tax": self.tax.to_dict() if self.tax else None,
            "total": self.total.to_dict() if self.total else None,
            "items": [item.to_dict() for item in self.items],
            "raw": self.raw,
        }


def field_value(value: Any, confidence: Any = 0.0) -> FieldValue:
    return FieldValue(value=value, confidence=_to_confidence(confidence))


def line_item(
    description: Optional[str] = None,
    quantity: Any = None,
    unit_price: Any = None,
    amount: Any = None,
    confidence: Any = 0.0,
) -> LineItem:
    return LineItem(
        description=description,
        quantity=_to_float(quantity),
        unit_price=_to_float(unit_price),
        amount=_to_float(amount),
        confidence=_to_confidence(confidence),
    )


def normalize_expense_payload(document: Dict[str, Any]) -> Dict[str, Any]:
    vendor_block = document.get("vendor") or document.get("merchant") or {}
    total_block = document.get("total") or {}
    tax_block = document.get("tax") or {}
    date_block = document.get("date") or {}
    normalized_items = []
    for item in document.get("items", []):
        normalized_items.append(
            {
                "description": item.get("description"),
                "quantity": _to_float(item.get("quantity")),
                "unit_price": _to_float(item.get("unit_price")),
                "amount": _to_float(item.get("amount")),
                "confidence": _to_confidence(item.get("confidence")),
            }
        )
    return {
        "expense_type": document.get("document_type"),
        "supplier": {
            "name": vendor_block.get("value"),
            "confidence": _to_confidence(vendor_block.get("confidence")),
        },
        "transaction_date": _normalize_date(date_block.get("value")),
        "amounts": {
            "tax": _to_float(tax_block.get("value")),
            "total": _to_float(total_block.get("value")),
        },
        "line_items": normalized_items,
        "source": {
            "provider": document.get("source_provider"),
            "model": document.get("source_model"),
        },
        "raw": document.get("raw", {}),
    }


def as_document_dict(document: ExtractedDocument) -> Dict[str, Any]:
    return document.to_dict()


def dataclass_to_dict(value: Any) -> Dict[str, Any]:
    return asdict(value)
