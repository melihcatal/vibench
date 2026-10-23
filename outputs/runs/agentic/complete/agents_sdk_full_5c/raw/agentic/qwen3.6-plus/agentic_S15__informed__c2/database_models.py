"""Local request, response, and normalization helpers for MongoDB Atlas Document Store."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class DocumentRequest:
    """Normalized request payload for document operations."""
    doc_id: str
    data: Dict[str, Any]
    version: Optional[int] = None
    partition_key: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.doc_id:
            self.doc_id = str(uuid.uuid4())
        if self.version is None:
            self.version = 1

    def to_mongo_document(self) -> Dict[str, Any]:
        """Convert to a MongoDB Atlas storage document."""
        doc = {
            "_id": self.doc_id,
            "version": self.version,
            "updated_at": _now_iso(),
        }
        doc.update(self.data)
        if self.partition_key is not None:
            doc["partition_key"] = self.partition_key
        return doc


@dataclass
class DocumentResponse:
    """Normalized response after document retrieval."""
    doc_id: str
    data: Dict[str, Any]
    version: int
    found: bool

    @classmethod
    def from_mongo(cls, doc: Optional[Dict[str, Any]]) -> "DocumentResponse":
        if doc is None:
            return cls(doc_id="", data={}, version=0, found=False)
        excluded = {"_id", "version", "updated_at", "partition_key"}
        data = {k: v for k, v in doc.items() if k not in excluded}
        return cls(
            doc_id=doc.get("_id", ""),
            data=data,
            version=doc.get("version", 0),
            found=True,
        )


@dataclass
class QueryResult:
    """Normalized batch query result."""
    documents: List[DocumentResponse] = field(default_factory=list)
    total_count: int = 0

    @classmethod
    def from_mongo_cursor(cls, cursor) -> "QueryResult":
        docs = list(cursor)
        responses = [DocumentResponse.from_mongo(d) for d in docs]
        return cls(documents=responses, total_count=len(responses))


def normalize_upsert_payload(raw: Dict[str, Any], doc_id: str) -> DocumentRequest:
    """Normalize a raw dict into a DocumentRequest ready for upsert."""
    version = raw.pop("version", None)
    partition_key = raw.pop("partition_key", None)
    return DocumentRequest(
        doc_id=doc_id,
        data=raw,
        version=version,
        partition_key=partition_key,
    )


def normalize_query_filter(field_name: str, field_value: Any) -> Dict[str, Any]:
    """Build a MongoDB Atlas query filter dict from a field name and value."""
    return {field_name: field_value}
