from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple, Union


JSONPrimitive = Union[str, int, float, bool, None]
JSONValue = Union[JSONPrimitive, Dict[str, Any], List[Any]]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalize_scalar(value: Any) -> JSONPrimitive:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Decimal):
        if value == value.to_integral_value():
            return int(value)
        return float(value)
    if isinstance(value, datetime):
        dt = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    return str(value)


def normalize_value(value: Any) -> JSONValue:
    if is_dataclass(value):
        return normalize_mapping(asdict(value))
    if isinstance(value, Mapping):
        return normalize_mapping(value)
    if isinstance(value, (list, tuple, set, frozenset)):
        return [normalize_value(item) for item in value]
    return _normalize_scalar(value)


def normalize_mapping(data: Mapping[str, Any]) -> Dict[str, JSONValue]:
    normalized: Dict[str, JSONValue] = {}
    for key, value in data.items():
        if value is None:
            continue
        normalized[str(key)] = normalize_value(value)
    return normalized


def _first_non_empty(*values: Any) -> Any:
    for value in values:
        if value is not None and value != "":
            return value
    return None


@dataclass
class DocumentKey:
    identifier: str
    partition_key: Optional[str] = None
    sort_key: Optional[str] = None

    def to_dict(self) -> Dict[str, JSONValue]:
        return normalize_mapping(asdict(self))


@dataclass
class DocumentEnvelope:
    identifier: str
    document: Dict[str, Any] = field(default_factory=dict)
    etag: Optional[str] = None
    version: Optional[Union[int, str]] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    partition_key: Optional[str] = None
    sort_key: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, JSONValue]:
        payload = asdict(self)
        payload["document"] = normalize_mapping(self.document)
        payload["metadata"] = normalize_mapping(self.metadata)
        return normalize_mapping(payload)


@dataclass
class RequestBase:
    request_id: Optional[str] = None
    client_timestamp: Optional[datetime] = None

    def common_fields(self) -> Dict[str, JSONValue]:
        payload = asdict(self)
        return normalize_mapping(payload)


@dataclass
class FetchDocumentRequest(RequestBase):
    identifier: str = ""
    partition_key: Optional[str] = None
    sort_key: Optional[str] = None
    consistent_read: bool = False


@dataclass
class QueryDocumentsRequest(RequestBase):
    field_name: str = ""
    field_value: Any = None
    partition_key: Optional[str] = None
    sort_key_prefix: Optional[str] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None
    consistent_read: bool = False


@dataclass
class UpsertDocumentRequest(RequestBase):
    identifier: str = ""
    document: Dict[str, Any] = field(default_factory=dict)
    partition_key: Optional[str] = None
    sort_key: Optional[str] = None
    expected_version: Optional[Union[int, str]] = None
    merge: bool = True


@dataclass
class ConditionalUpdateRequest(RequestBase):
    identifier: str = ""
    updates: Dict[str, Any] = field(default_factory=dict)
    condition: Dict[str, Any] = field(default_factory=dict)
    partition_key: Optional[str] = None
    sort_key: Optional[str] = None
    expected_version: Optional[Union[int, str]] = None
    return_document: bool = True


@dataclass
class QueryDocumentsResponse:
    items: List[DocumentEnvelope] = field(default_factory=list)
    count: int = 0
    cursor: Optional[str] = None
    scanned_count: Optional[int] = None

    def to_dict(self) -> Dict[str, JSONValue]:
        return {
            "items": [item.to_dict() for item in self.items],
            "count": self.count,
            "cursor": self.cursor,
            "scanned_count": self.scanned_count,
        }


@dataclass
class FetchDocumentResponse:
    item: Optional[DocumentEnvelope] = None
    found: bool = False

    def to_dict(self) -> Dict[str, JSONValue]:
        return {"item": None if self.item is None else self.item.to_dict(), "found": self.found}


@dataclass
class UpsertDocumentResponse:
    item: DocumentEnvelope
    created: bool = False

    def to_dict(self) -> Dict[str, JSONValue]:
        return {"item": self.item.to_dict(), "created": self.created}


@dataclass
class ConditionalUpdateResponse:
    item: Optional[DocumentEnvelope] = None
    applied: bool = False
    matched: bool = False

    def to_dict(self) -> Dict[str, JSONValue]:
        return {
            "item": None if self.item is None else self.item.to_dict(),
            "applied": self.applied,
            "matched": self.matched,
        }


def infer_document_identifier(document: Mapping[str, Any]) -> Optional[str]:
    for candidate in ("id", "identifier", "_id", "document_id", "record_id"):
        value = document.get(candidate)
        if value is not None and value != "":
            return str(value)
    return None


def build_document_envelope(
    document: Mapping[str, Any],
    *,
    identifier: Optional[str] = None,
    etag: Optional[str] = None,
    version: Optional[Union[int, str]] = None,
    partition_key: Optional[str] = None,
    sort_key: Optional[str] = None,
    metadata: Optional[Mapping[str, Any]] = None,
    created_at: Optional[datetime] = None,
    updated_at: Optional[datetime] = None,
) -> DocumentEnvelope:
    resolved_identifier = _first_non_empty(identifier, infer_document_identifier(document), _utc_now_iso())
    return DocumentEnvelope(
        identifier=str(resolved_identifier),
        document=dict(document),
        etag=etag,
        version=version,
        updated_at=updated_at,
        created_at=created_at,
        partition_key=partition_key,
        sort_key=sort_key,
        metadata=dict(metadata or {}),
    )


def response_item_to_dict(item: Optional[DocumentEnvelope]) -> Optional[Dict[str, JSONValue]]:
    return None if item is None else item.to_dict()


def request_to_dict(request: Any) -> Dict[str, JSONValue]:
    if hasattr(request, "common_fields") and callable(getattr(request, "common_fields")):
        return request.common_fields()
    if is_dataclass(request):
        return normalize_mapping(asdict(request))
    if isinstance(request, Mapping):
        return normalize_mapping(request)
    raise TypeError(f"Unsupported request type: {type(request)!r}")
