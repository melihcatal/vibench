import os
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from datetime import datetime


@dataclass
class DocumentRequest:
    collection: str
    document_id: str
    data: dict
    partition_key: Optional[str] = None
    version: Optional[int] = None
    condition: Optional[dict] = None


@dataclass
class DocumentResponse:
    document_id: str
    data: dict
    collection: str
    version: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    metadata: dict = field(default_factory=dict)


@dataclass
class QueryRequest:
    collection: str
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None
    limit: int = 100
    sort_field: Optional[str] = None
    sort_order: int = 1


@dataclass
class UpdateResult:
    success: bool
    document_id: str
    matched_count: int = 0
    modified_count: int = 0
    upserted_id: Optional[str] = None
    version: Optional[int] = None
    message: str = ""


@dataclass
class ArchiveRecord:
    archive_id: str
    source_collection: str
    document_ids: list
    storage_key: str
    archived_at: str
    size_bytes: int = 0


def normalize_document(raw: dict, doc_id_field: str = "_id") -> dict:
    normalized = {}
    for key, value in raw.items():
        if key == doc_id_field and isinstance(value, dict):
            normalized["document_id"] = str(value.get("$oid", value))
        elif isinstance(value, datetime):
            normalized[key] = value.isoformat()
        else:
            normalized[key] = value
    if "document_id" not in normalized and doc_id_field in raw:
        normalized["document_id"] = str(raw[doc_id_field])
    return normalized


def build_mongo_filter(request: DocumentRequest) -> dict:
    query_filter = {"_id": request.document_id}
    if request.partition_key:
        query_filter["partition_key"] = request.partition_key
    if request.condition:
        query_filter.update(request.condition)
    return query_filter


def build_query_filter(request: QueryRequest) -> dict:
    query_filter = {request.field_name: request.field_value}
    if request.partition_key:
        query_filter["partition_key"] = request.partition_key
    return query_filter


def prepare_upsert_payload(request: DocumentRequest) -> dict:
    now = datetime.utcnow().isoformat()
    payload = {**request.data}
    payload["_id"] = request.document_id
    payload["partition_key"] = request.partition_key or "default"
    payload.setdefault("created_at", now)
    payload["updated_at"] = now
    if request.version is not None:
        payload["version"] = request.version
    else:
        payload["version"] = 1
    return payload


def to_document_response(raw_doc: dict, collection: str) -> DocumentResponse:
    normalized = normalize_document(raw_doc)
    return DocumentResponse(
        document_id=normalized.get("document_id", ""),
        data={k: v for k, v in normalized.items() if k != "document_id"},
        collection=collection,
        version=normalized.get("version", 0),
        created_at=normalized.get("created_at"),
        updated_at=normalized.get("updated_at"),
        metadata={k: v for k, v in normalized.items() if k.startswith("_meta_")},
    )
