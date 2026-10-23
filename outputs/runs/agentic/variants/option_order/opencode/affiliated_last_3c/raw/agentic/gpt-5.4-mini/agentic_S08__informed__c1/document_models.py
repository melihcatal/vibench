from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    document_bytes: bytes
    content_type: str = "application/pdf"
    model_id: str = "prebuilt-invoice"


@dataclass
class FieldValue:
    value: Any
    confidence: Optional[float] = None


@dataclass
class DocumentResponse:
    fields: Dict[str, FieldValue] = field(default_factory=dict)
    raw: Optional[Dict[str, Any]] = None


def normalize_field_value(value: Any) -> Any:
    if isinstance(value, dict):
        for key in ("content", "value", "text"):
            if key in value:
                return value[key]
    return value


def extract_confidence(field: Any) -> Optional[float]:
    if isinstance(field, dict):
        confidence = field.get("confidence")
        if confidence is not None:
            return float(confidence)
    return None


def build_standard_expense_record(source: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "vendor": normalize_field_value(source.get("vendor")),
        "date": normalize_field_value(source.get("date")),
        "total": normalize_field_value(source.get("total")),
        "tax": normalize_field_value(source.get("tax")),
        "items": source.get("items", []),
        "confidence": {
            key: extract_confidence(value)
            for key, value in source.items()
            if isinstance(value, dict)
        },
    }
