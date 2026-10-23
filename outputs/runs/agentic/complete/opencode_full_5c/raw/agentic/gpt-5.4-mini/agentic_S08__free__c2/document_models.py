from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    source_uri: str
    document_type: str
    schema_name: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentField:
    name: str
    value: Any
    confidence: Optional[float] = None


@dataclass
class DocumentResponse:
    document_type: str
    fields: List[DocumentField]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedExpenseRecord:
    vendor: str
    transaction_date: str
    currency: str
    total_amount: float
    tax_amount: float
    line_items: List[Dict[str, Any]]
    source_document_id: Optional[str] = None


def coerce_confidence(value: Any) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def as_field_map(fields: List[DocumentField]) -> Dict[str, Any]:
    return {field.name: field.value for field in fields}
