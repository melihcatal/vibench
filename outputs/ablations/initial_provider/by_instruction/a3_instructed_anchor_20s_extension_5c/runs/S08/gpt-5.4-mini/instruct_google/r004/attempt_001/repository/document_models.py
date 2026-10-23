from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StructuredField:
    name: str
    value: Any
    confidence: float = 0.0


@dataclass
class ExtractionResult:
    source: str
    fields: Dict[str, StructuredField] = field(default_factory=dict)


def normalize_field_map(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        key: value.value if isinstance(value, StructuredField) else value
        for key, value in payload.items()
    }


def standard_expense_schema(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "vendor": payload.get("vendor", ""),
        "date": payload.get("date", ""),
        "total": payload.get("total", ""),
        "currency": payload.get("currency", ""),
        "line_items": payload.get("line_items", []),
        "tax": payload.get("tax", ""),
        "merchant": payload.get("merchant", ""),
        "items": payload.get("items", []),
        "notes": payload.get("notes", ""),
    }
