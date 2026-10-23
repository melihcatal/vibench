from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentImageInput:
    uri: str
    mime_type: str = "image/png"


@dataclass
class StructuredExtractionRequest:
    source_uri: str
    mime_type: str = "application/pdf"
    schema_name: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StructuredExtractionResponse:
    fields: Dict[str, Any]
    confidence: Dict[str, float] = field(default_factory=dict)
    raw: Optional[Dict[str, Any]] = None


def normalize_money(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "")
    if text.startswith("$"):
        text = text[1:]
    try:
        return float(text)
    except ValueError:
        return None


def normalize_text(value: Any) -> str:
    return "" if value is None else str(value).strip()
