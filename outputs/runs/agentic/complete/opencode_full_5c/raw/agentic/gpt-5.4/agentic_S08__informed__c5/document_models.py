from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class ExtractedField:
    value: Any
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {"value": self.value, "confidence": float(self.confidence)}


@dataclass
class LineItem:
    description: str = ""
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "amount": self.amount,
            "confidence": float(self.confidence),
        }


@dataclass
class ExtractionResult:
    document_type: str
    provider: str
    fields: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_type": self.document_type,
            "provider": self.provider,
            "fields": self.fields,
            "line_items": self.line_items,
            "raw_response": self.raw_response,
        }


@dataclass
class ValidationIssue:
    field: str
    message: str

    def to_dict(self) -> Dict[str, Any]:
        return {"field": self.field, "message": self.message}


@dataclass
class ValidationResult:
    valid: bool
    issues: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {"valid": self.valid, "issues": self.issues}


def field_dict(value: Any, confidence: Optional[float] = None) -> Dict[str, Any]:
    payload = {"value": value}
    if confidence is not None:
        payload["confidence"] = float(confidence)
    return payload


def safe_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_line_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "description": item.get("description") or "",
        "quantity": safe_float(item.get("quantity")),
        "unit_price": safe_float(item.get("unit_price")),
        "amount": safe_float(item.get("amount")),
        "confidence": float(item.get("confidence", 0.0) or 0.0),
    }


def normalize_expense_record(extracted: Dict[str, Any]) -> Dict[str, Any]:
    fields = extracted.get("fields", {})
    line_items = extracted.get("line_items", [])
    record_id = extracted.get("record_id") or str(uuid.uuid4())
    return {
        "id": record_id,
        "source_document_type": extracted.get("document_type"),
        "provider": extracted.get("provider"),
        "vendor": fields.get("vendor", {}).get("value")
        or fields.get("merchant", {}).get("value"),
        "document_date": fields.get("date", {}).get("value"),
        "currency": fields.get("currency", {}).get("value"),
        "subtotal": safe_float(fields.get("subtotal", {}).get("value")),
        "tax": safe_float(fields.get("tax", {}).get("value")),
        "total": safe_float(fields.get("total", {}).get("value")),
        "notes": fields.get("notes", {}).get("value")
        or fields.get("memo", {}).get("value"),
        "line_items": [normalize_line_item(item) for item in line_items],
        "confidence": {
            key: float(value.get("confidence", 0.0) or 0.0)
            for key, value in fields.items()
            if isinstance(value, dict)
        },
    }
