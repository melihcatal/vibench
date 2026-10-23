import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, Mapping, MutableMapping, Optional


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    if isinstance(value, tuple):
        return [_jsonable(v) for v in value]
    if isinstance(value, set):
        return sorted(_jsonable(v) for v in value)
    try:
        json.dumps(value)
        return value
    except TypeError:
        return str(value)


def normalize_document(document: Any) -> Dict[str, Any]:
    if isinstance(document, str):
        document = json.loads(document)
    if not isinstance(document, Mapping):
        raise ValueError("document must be a JSON object")
    return {str(key): _jsonable(value) for key, value in document.items()}


def normalize_documents(documents: Iterable[Any]) -> list[Dict[str, Any]]:
    return [normalize_document(document) for document in documents]


def coerce_primary_key(document: Mapping[str, Any], primary_key_field: str = "_id") -> Any:
    if primary_key_field not in document:
        raise ValueError(f"Missing primary key field: {primary_key_field}")
    return document[primary_key_field]


@dataclass(frozen=True)
class DocumentRequest:
    document: Dict[str, Any]
    primary_key_field: str = "_id"

    @classmethod
    def from_value(cls, value: Any, primary_key_field: str = "_id") -> "DocumentRequest":
        return cls(document=normalize_document(value), primary_key_field=primary_key_field)

    def primary_key(self) -> Any:
        return coerce_primary_key(self.document, self.primary_key_field)

    def to_dict(self) -> Dict[str, Any]:
        return {"document": self.document, "primary_key_field": self.primary_key_field}


@dataclass(frozen=True)
class UpsertRequest(DocumentRequest):
    upsert: bool = True

    def to_dict(self) -> Dict[str, Any]:
        payload = super().to_dict()
        payload["upsert"] = self.upsert
        return payload


@dataclass(frozen=True)
class QueryRequest:
    field_name: str
    field_value: Any
    partition_key_name: Optional[str] = None
    limit: Optional[int] = None
    index_name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field_name": self.field_name,
            "field_value": _jsonable(self.field_value),
            "partition_key_name": self.partition_key_name,
            "limit": self.limit,
            "index_name": self.index_name,
        }


@dataclass(frozen=True)
class FetchRequest:
    document_id: Any

    def to_dict(self) -> Dict[str, Any]:
        return {"document_id": _jsonable(self.document_id)}


@dataclass(frozen=True)
class ConditionRequest(DocumentRequest):
    expected_version: Optional[int] = None
    version_field: str = "version"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document": self.document,
            "primary_key_field": self.primary_key_field,
            "expected_version": self.expected_version,
            "version_field": self.version_field,
        }


@dataclass(frozen=True)
class OperationResponse:
    ok: bool = True
    message: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_value(cls, value: Mapping[str, Any], ok: bool = True, message: Optional[str] = None) -> "OperationResponse":
        return cls(ok=ok, message=message, raw={str(k): _jsonable(v) for k, v in value.items()})

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DocumentResponse(OperationResponse):
    document: Optional[Dict[str, Any]] = None

    @classmethod
    def from_document(cls, document: Any, ok: bool = True, message: Optional[str] = None, raw: Optional[Mapping[str, Any]] = None) -> "DocumentResponse":
        return cls(ok=ok, message=message, raw={str(k): _jsonable(v) for k, v in (raw or {}).items()}, document=normalize_document(document) if document is not None else None)


@dataclass(frozen=True)
class QueryResponse(OperationResponse):
    items: list[Dict[str, Any]] = field(default_factory=list)
    count: int = 0

    @classmethod
    def from_items(cls, items: Iterable[Any], ok: bool = True, message: Optional[str] = None, raw: Optional[Mapping[str, Any]] = None) -> "QueryResponse":
        normalized_items = normalize_documents(items)
        return cls(ok=ok, message=message, raw={str(k): _jsonable(v) for k, v in (raw or {}).items()}, items=normalized_items, count=len(normalized_items))


@dataclass(frozen=True)
class UpsertResponse(OperationResponse):
    matched_count: int = 0
    modified_count: int = 0
    upserted_id: Optional[Any] = None

    @classmethod
    def from_result(cls, result: Mapping[str, Any], ok: bool = True, message: Optional[str] = None) -> "UpsertResponse":
        return cls(
            ok=ok,
            message=message,
            raw={str(k): _jsonable(v) for k, v in result.items()},
            matched_count=int(result.get("matchedCount", 0) or 0),
            modified_count=int(result.get("modifiedCount", 0) or 0),
            upserted_id=result.get("upsertedId"),
        )


@dataclass(frozen=True)
class ConditionalUpdateResponse(OperationResponse):
    matched_count: int = 0
    modified_count: int = 0
    updated: bool = False
    reason: Optional[str] = None
    upserted_id: Optional[Any] = None

    @classmethod
    def from_result(cls, result: Mapping[str, Any], updated: Optional[bool] = None, reason: Optional[str] = None, ok: bool = True, message: Optional[str] = None) -> "ConditionalUpdateResponse":
        matched_count = int(result.get("matchedCount", 0) or 0)
        modified_count = int(result.get("modifiedCount", 0) or 0)
        return cls(
            ok=ok,
            message=message,
            raw={str(k): _jsonable(v) for k, v in result.items()},
            matched_count=matched_count,
            modified_count=modified_count,
            updated=bool(updated if updated is not None else modified_count),
            reason=reason,
            upserted_id=result.get("upsertedId"),
        )


def response_from_dict(payload: MutableMapping[str, Any]) -> OperationResponse:
    payload = dict(payload)
    if "items" in payload:
        return QueryResponse.from_items(payload.get("items", []), ok=bool(payload.get("ok", True)), message=payload.get("message"), raw=payload)
    if "document" in payload:
        return DocumentResponse.from_document(payload.get("document"), ok=bool(payload.get("ok", True)), message=payload.get("message"), raw=payload)
    if "updated" in payload or "reason" in payload:
        return ConditionalUpdateResponse(
            ok=bool(payload.get("ok", True)),
            message=payload.get("message"),
            raw={str(k): _jsonable(v) for k, v in payload.items()},
            matched_count=int(payload.get("matched_count", 0) or 0),
            modified_count=int(payload.get("modified_count", 0) or 0),
            updated=bool(payload.get("updated", False)),
            reason=payload.get("reason"),
            upserted_id=payload.get("upserted_id"),
        )
    return OperationResponse.from_value(payload, ok=bool(payload.get("ok", True)), message=payload.get("message"))


__all__ = [
    "ConditionRequest",
    "ConditionalUpdateResponse",
    "DocumentRequest",
    "DocumentResponse",
    "FetchRequest",
    "OperationResponse",
    "QueryRequest",
    "QueryResponse",
    "UpsertRequest",
    "UpsertResponse",
    "coerce_primary_key",
    "normalize_document",
    "normalize_documents",
    "response_from_dict",
]
