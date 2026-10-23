from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DocumentExtractionRequest:
    document_text: str
    document_type: str
    locale: str = "en"


@dataclass
class DocumentExtractionResponse:
    fields: Dict[str, Any]
    raw: Dict[str, Any]


@dataclass
class NormalizedExpenseRecord:
    merchant: str
    date: Optional[str]
    total: Optional[float]
    tax: Optional[float]
    currency: Optional[str]
    items: List[Dict[str, Any]]


def normalize_money(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "")
    for prefix in ("$", "€", "£"):
        text = text.replace(prefix, "")
    try:
        return float(text)
    except ValueError:
        return None


def normalize_items(items: Any) -> List[Dict[str, Any]]:
    if not isinstance(items, list):
        return []
    normalized = []
    for item in items:
        if isinstance(item, dict):
            normalized.append(item)
    return normalized
