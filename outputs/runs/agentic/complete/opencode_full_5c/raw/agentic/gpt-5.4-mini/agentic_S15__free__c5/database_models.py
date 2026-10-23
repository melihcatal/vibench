from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, Mapping


def normalize_value(value: Any) -> Any:
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, dict):
        return {str(k): normalize_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize_value(v) for v in value]
    return value


def normalize_document(document: Mapping[str, Any]) -> Dict[str, Any]:
    return {str(k): normalize_value(v) for k, v in document.items()}


@dataclass(frozen=True)
class DocumentRequest:
    document_id: str
    document: Dict[str, Any]


@dataclass(frozen=True)
class QueryRequest:
    field_name: str
    field_value: Any


@dataclass(frozen=True)
class UpdateRequest:
    document_id: str
    updates: Dict[str, Any]
    version: int | None = None
