from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional


@dataclass
class FieldValue:
    value: Any
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {"value": self.value, "confidence": self.confidence}


@dataclass
class LineItem:
    description: str = ""
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExtractedDocument:
    document_type: str
    source_uri: Optional[str] = None
    raw_provider_response: Dict[str, Any] = field(default_factory=dict)
    fields: Dict[str, FieldValue] = field(default_factory=dict)
    items: List[LineItem] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_type": self.document_type,
            "source_uri": self.source_uri,
            "fields": {k: v.to_dict() for k, v in self.fields.items()},
            "items": [item.to_dict() for item in self.items],
            "raw_provider_response": self.raw_provider_response,
        }


def parse_decimal(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(Decimal(str(value).replace(",", "")))
    except (InvalidOperation, ValueError):
        return None


def parse_date(value: Any) -> Optional[str]:
    if value is None or value == "":
        return None
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    return text


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def build_standard_expense_schema(
    document_type: str, extracted: Dict[str, Any]
) -> Dict[str, Any]:
    fields = extracted.get("fields", {})
    items = extracted.get("items", [])
    vendor_name = normalize_text(
        fields.get("vendor", {}).get("value") or fields.get("merchant", {}).get("value")
    )
    total_amount = parse_decimal(fields.get("total", {}).get("value"))
    tax_amount = parse_decimal(fields.get("tax", {}).get("value"))
    document_date = parse_date(fields.get("date", {}).get("value"))
    normalized_items = []
    for item in items:
        normalized_items.append(
            {
                "description": normalize_text(item.get("description")),
                "quantity": parse_decimal(item.get("quantity")),
                "unit_price": parse_decimal(item.get("unit_price")),
                "amount": parse_decimal(item.get("amount")),
                "confidence": float(item.get("confidence", 0.0)),
            }
        )
    return {
        "document_type": document_type,
        "vendor_name": vendor_name,
        "document_date": document_date,
        "currency": normalize_text(fields.get("currency", {}).get("value")) or "USD",
        "subtotal": parse_decimal(fields.get("subtotal", {}).get("value")),
        "tax": tax_amount,
        "total": total_amount,
        "items": normalized_items,
        "source_uri": extracted.get("source_uri"),
        "provider": extracted.get("provider"),
    }
