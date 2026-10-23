from dataclasses import dataclass, field, asdict
from typing import Any, Optional


@dataclass
class DocumentUpsertRequest:
    collection: str
    document_id: str
    data: dict[str, Any]
    partition_key: Optional[str] = None


@dataclass
class DocumentFetchRequest:
    collection: str
    document_id: str


@dataclass
class DocumentQueryRequest:
    collection: str
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None
    limit: int = 100


@dataclass
class ConditionalUpdateRequest:
    collection: str
    document_id: str
    updates: dict[str, Any]
    condition_field: str
    condition_value: Any


@dataclass
class DocumentResponse:
    document_id: str
    data: dict[str, Any]
    collection: str
    version: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class QueryResponse:
    documents: list[DocumentResponse]
    total_count: int


@dataclass
class UpdateResponse:
    document_id: str
    matched: bool
    modified: bool
    version: Optional[str] = None


def normalize_upsert_payload(request: DocumentUpsertRequest) -> dict[str, Any]:
    payload = {"_id": request.document_id}
    payload.update(request.data)
    if request.partition_key:
        payload["partition_key"] = request.partition_key
    return payload


def normalize_document_response(raw_doc: dict, collection: str) -> DocumentResponse:
    doc_id = raw_doc.pop("_id", raw_doc.get("document_id", ""))
    version = raw_doc.pop("_version", raw_doc.get("version", None))
    return DocumentResponse(
        document_id=str(doc_id),
        data=raw_doc,
        collection=collection,
        version=version,
    )


def normalize_query_response(raw_docs: list[dict], collection: str) -> QueryResponse:
    documents = [normalize_document_response(doc, collection) for doc in raw_docs]
    return QueryResponse(documents=documents, total_count=len(documents))


def serialize_for_storage(doc_response: DocumentResponse) -> dict[str, Any]:
    result = asdict(doc_response)
    return result
