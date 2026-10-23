from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Mapping, Optional, Sequence


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _clean_mapping(value: Mapping[str, Any]) -> Dict[str, Any]:
    return {k: normalize_document(v) for k, v in value.items() if v is not None}


def normalize_document(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if is_dataclass(value):
        return normalize_document(asdict(value))
    if isinstance(value, Mapping):
        return _clean_mapping(value)
    if isinstance(value, (list, tuple, set)):
        return [normalize_document(item) for item in value]
    return value


def denormalize_document(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: denormalize_document(v) for k, v in value.items()}
    if isinstance(value, list):
        return [denormalize_document(item) for item in value]
    return value


@dataclass
class DocumentMetadata:
    id: str
    partition_key: Optional[str] = None
    version: Optional[str] = None
    etag: Optional[str] = None
    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)

    def to_dict(self) -> Dict[str, Any]:
        return normalize_document(asdict(self))


@dataclass
class DocumentRequest:
    document: Dict[str, Any]
    id_field: str = "id"
    partition_key_field: Optional[str] = None

    def normalized(self) -> Dict[str, Any]:
        return normalize_document(self.document)

    def document_id(self) -> str:
        value = self.document.get(self.id_field)
        if value is None:
            raise ValueError(f"missing required identifier field: {self.id_field}")
        return str(value)

    def partition_key_value(self) -> Optional[str]:
        if not self.partition_key_field:
            return None
        value = self.document.get(self.partition_key_field)
        return None if value is None else str(value)


@dataclass
class UpsertDocumentRequest(DocumentRequest):
    pass


@dataclass
class ConditionalUpdateRequest(DocumentRequest):
    expected_version: Optional[str] = None
    expected_etag: Optional[str] = None
    patch: Optional[Dict[str, Any]] = None

    def has_condition(self) -> bool:
        return self.expected_version is not None or self.expected_etag is not None

    def normalized_patch(self) -> Optional[Dict[str, Any]]:
        return None if self.patch is None else normalize_document(self.patch)


@dataclass
class FetchDocumentRequest:
    document_id: str
    partition_key: Optional[str] = None


@dataclass
class QueryDocumentsRequest:
    field_name: str
    field_value: Any
    limit: Optional[int] = None
    partition_key: Optional[str] = None

    def normalized_field_value(self) -> Any:
        return normalize_document(self.field_value)


@dataclass
class DocumentResponse:
    document: Dict[str, Any]
    metadata: Optional[DocumentMetadata] = None

    def normalized_document(self) -> Dict[str, Any]:
        return normalize_document(self.document)


@dataclass
class QueryDocumentsResponse:
    items: Sequence[DocumentResponse] = field(default_factory=list)


@dataclass
class OperationStatus:
    ok: bool
    message: str = ""
    metadata: Optional[DocumentMetadata] = None


def extract_document_id(document: Mapping[str, Any], id_field: str = "id") -> str:
    value = document.get(id_field)
    if value is None:
        raise ValueError(f"missing required identifier field: {id_field}")
    return str(value)


def extract_partition_key(document: Mapping[str, Any], partition_key_field: Optional[str]) -> Optional[str]:
    if not partition_key_field:
        return None
    value = document.get(partition_key_field)
    return None if value is None else str(value)


def merge_documents(base: Mapping[str, Any], updates: Mapping[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    for key, value in updates.items():
        if value is None:
            continue
        if isinstance(value, Mapping) and isinstance(merged.get(key), Mapping):
            merged[key] = merge_documents(merged[key], value)
        else:
            merged[key] = normalize_document(value)
    return merged


def build_document_response(document: Mapping[str, Any], metadata: Optional[Mapping[str, Any]] = None) -> DocumentResponse:
    meta = None
    if metadata is not None:
        meta = DocumentMetadata(
            id=str(metadata.get("id", extract_document_id(document))),
            partition_key=metadata.get("partition_key"),
            version=metadata.get("version"),
            etag=metadata.get("etag"),
            created_at=metadata.get("created_at", _utc_now()),
            updated_at=metadata.get("updated_at", _utc_now()),
        )
    return DocumentResponse(document=normalize_document(document), metadata=meta)


def coerce_document_list(items: Iterable[Mapping[str, Any]]) -> Sequence[DocumentResponse]:
    return [build_document_response(item) for item in items]
