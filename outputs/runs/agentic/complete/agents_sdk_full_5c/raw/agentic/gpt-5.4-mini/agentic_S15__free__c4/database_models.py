from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional

from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

_serializer = TypeSerializer()
_deserializer = TypeDeserializer()


@dataclass
class DocumentKey:
    document_id: str


@dataclass
class DocumentRecord:
    document_id: str
    payload: Dict[str, Any] = field(default_factory=dict)
    version: Optional[int] = None


@dataclass
class OperationResult:
    ok: bool
    message: str
    item: Optional[Dict[str, Any]] = None


def _normalize_value(value: Any) -> Any:
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, dict):
        return {str(k): _normalize_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize_value(v) for v in value]
    return value


def normalize_document(document: Mapping[str, Any]) -> Dict[str, Any]:
    normalized = {str(k): _normalize_value(v) for k, v in document.items()}
    return normalized


def serialize_item(item: Mapping[str, Any]) -> Dict[str, Any]:
    return {key: _serializer.serialize(_normalize_value(value)) for key, value in item.items()}


def deserialize_item(item: Mapping[str, Any]) -> Dict[str, Any]:
    return {key: _deserializer.deserialize(value) for key, value in item.items()}


def compact_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def extract_field_text(document: Mapping[str, Any], fields: Iterable[str]) -> str:
    parts: List[str] = []
    for field in fields:
        if field in document:
            parts.append(compact_text(document[field]))
    return " ".join(part for part in parts if part)
