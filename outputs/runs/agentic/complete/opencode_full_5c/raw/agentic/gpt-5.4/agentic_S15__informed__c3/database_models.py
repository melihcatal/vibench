from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional


@dataclass
class DocumentRecord:
    document_id: str
    partition_key: Optional[str]
    version: Optional[int]
    data: Dict[str, Any]


@dataclass
class UpsertResult:
    document_id: str
    partition_key: Optional[str]
    etag: Optional[str]
    request_charge: Optional[float]
    body: Dict[str, Any]


@dataclass
class FetchResult:
    found: bool
    document_id: str
    partition_key: Optional[str]
    etag: Optional[str]
    body: Optional[Dict[str, Any]]


@dataclass
class QueryResult:
    items: List[Dict[str, Any]]
    count: int


@dataclass
class ConditionalUpdateResult:
    updated: bool
    document_id: str
    partition_key: Optional[str]
    etag: Optional[str]
    body: Optional[Dict[str, Any]]


def normalize_document(
    document: Dict[str, Any], document_id_field: str = "id"
) -> Dict[str, Any]:
    normalized = dict(document)
    if document_id_field not in normalized or normalized[document_id_field] in (
        None,
        "",
    ):
        raise ValueError("document must contain a non-empty id field")
    normalized[document_id_field] = str(normalized[document_id_field])
    return normalized


def extract_partition_key(
    document: Dict[str, Any], partition_field: str
) -> Optional[str]:
    value = document.get(partition_field)
    if value is None:
        return None
    return str(value)


def to_document_record(
    document: Dict[str, Any], partition_field: str = "partition_key"
) -> DocumentRecord:
    return DocumentRecord(
        document_id=str(document["id"]),
        partition_key=extract_partition_key(document, partition_field),
        version=document.get("version"),
        data=dict(document),
    )


def normalize_documents(
    documents: Iterable[Dict[str, Any]], partition_field: str = "partition_key"
) -> List[Dict[str, Any]]:
    return [
        to_document_record(item, partition_field=partition_field).data
        for item in documents
    ]


def build_summary_text(
    document: Dict[str, Any], fields: Optional[Iterable[str]] = None
) -> str:
    selected_fields = (
        list(fields) if fields else ["id", "title", "status", "category", "content"]
    )
    parts: List[str] = []
    for field in selected_fields:
        value = document.get(field)
        if value is None:
            continue
        parts.append(f"{field}: {value}")
    return "\n".join(parts)


def collect_text_fields(
    document: Dict[str, Any], fields: Iterable[str]
) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for field in fields:
        value = document.get(field)
        if isinstance(value, str) and value.strip():
            result[field] = value
    return result
