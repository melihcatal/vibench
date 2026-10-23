from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    document_bytes: Optional[bytes] = None
    document_uri: Optional[str] = None
    document_text: Optional[str] = None


@dataclass
class FieldConfidence:
    value: Any
    confidence: float


@dataclass
class NormalizedExpenseRecord:
    vendor: str
    date: str
    total: float
    tax: float
    currency: str
    items: List[Dict[str, Any]]


def to_dict(instance: Any) -> Dict[str, Any]:
    return asdict(instance)


def coerce_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def coerce_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []
