from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from datetime import datetime, timezone


@dataclass
class DocumentUpsertRequest:
    document_id: str
    data: dict[str, Any]
    partition_key: Optional[str] = None
    ttl_seconds: Optional[int] = None


@dataclass
class DocumentFetchRequest:
    document_id: str
    partition_key: Optional[str] = None


@dataclass
class DocumentQueryRequest:
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None
    limit: int = 50
    sort_field: Optional[str] = None
    sort_order: int = -1


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    updates: dict[str, Any]
    condition_field: Optional[str] = None
    condition_value: Optional[Any] = None
    partition_key: Optional[str] = None


@dataclass
class DocumentResponse:
    document_id: str
    data: dict[str, Any]
    partition_key: Optional[str] = None
    version: int = 1
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    found: bool = True


@dataclass
class QueryResponse:
    documents: list[DocumentResponse]
    total_count: int
    has_more: bool = False


@dataclass
class UpdateResponse:
    document_id: str
    matched: bool
    modified: bool
    version: int = 1
    condition_met: bool = True


def normalize_document(
    raw_doc: dict[str, Any], document_id_field: str = "_id"
) -> DocumentResponse:
    doc_id = str(raw_doc.pop(document_id_field, raw_doc.get("document_id", "")))
    version = raw_doc.pop("version", 1)
    created_at = raw_doc.pop("created_at", None)
    updated_at = raw_doc.pop("updated_at", None)
    partition_key = raw_doc.pop("partition_key", None)
    if created_at and isinstance(created_at, datetime):
        created_at = created_at.isoformat()
    if updated_at and isinstance(updated_at, datetime):
        updated_at = updated_at.isoformat()
    return DocumentResponse(
        document_id=doc_id,
        data=dict(raw_doc),
        partition_key=partition_key,
        version=version,
        created_at=created_at,
        updated_at=updated_at,
    )


def build_upsert_payload(request: DocumentUpsertRequest) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    payload = {
        "document_id": request.document_id,
        **request.data,
        "updated_at": now,
        "version": 1,
    }
    if request.partition_key:
        payload["partition_key"] = request.partition_key
    if request.ttl_seconds:
        from datetime import timedelta

        payload["expires_at"] = now + timedelta(seconds=request.ttl_seconds)
    return payload


def build_update_set_fields(request: ConditionalUpdateRequest) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    set_fields = dict(request.updates)
    set_fields["updated_at"] = now
    return set_fields
