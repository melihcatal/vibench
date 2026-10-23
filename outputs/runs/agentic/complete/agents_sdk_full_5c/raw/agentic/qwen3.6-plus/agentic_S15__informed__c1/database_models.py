"""
Local request, response, and normalization helpers for MongoDB Atlas
managed NoSQL document store operations.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime


@dataclass
class DocumentRequest:
    """Represents an upsert or conditional-update request."""
    document_id: str
    data: Dict[str, Any]
    partition_key: Optional[str] = None
    version: Optional[int] = None
    conditional_match: Optional[Dict[str, Any]] = None

    def to_payload(self) -> Dict[str, Any]:
        payload = {"document_id": self.document_id}
        payload.update(self.data)
        if self.partition_key is not None:
            payload["partition_key"] = self.partition_key
        if self.version is not None:
            payload["_version"] = self.version
        return payload


@dataclass
class DocumentResponse:
    """Represents a fetched or queried document response."""
    document_id: str
    data: Dict[str, Any]
    partition_key: Optional[str] = None
    version: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"document_id": self.document_id}
        result.update(self.data)
        if self.partition_key is not None:
            result["partition_key"] = self.partition_key
        if self.version is not None:
            result["_version"] = self.version
        if self.created_at is not None:
            result["created_at"] = self.created_at.isoformat()
        if self.updated_at is not None:
            result["updated_at"] = self.updated_at.isoformat()
        return result


@dataclass
class QueryResult:
    """Container for a list of DocumentResponse objects returned from a query."""
    documents: List[DocumentResponse] = field(default_factory=list)
    total_count: int = 0

    def to_list(self) -> List[Dict[str, Any]]:
        return [doc.to_dict() for doc in self.documents]


def parse_raw_to_response(raw_doc: Dict[str, Any]) -> DocumentResponse:
    """Convert a raw MongoDB document dict into a DocumentResponse."""
    if raw_doc is None:
        raise ValueError("Received None document")

    doc_id = str(raw_doc.get("document_id", raw_doc.get("_id", "")))
    data = {k: v for k, v in raw_doc.items() if k not in (
        "_id", "document_id", "partition_key", "_version",
        "created_at", "updated_at"
    )}
    partition_key = raw_doc.get("partition_key")
    version = raw_doc.get("_version")

    created_at = None
    updated_at = None
    if isinstance(raw_doc.get("created_at"), datetime):
        created_at = raw_doc["created_at"]
    if isinstance(raw_doc.get("updated_at"), datetime):
        updated_at = raw_doc["updated_at"]

    return DocumentResponse(
        document_id=doc_id,
        data=data,
        partition_key=partition_key,
        version=version,
        created_at=created_at,
        updated_at=updated_at,
    )


def build_update_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    """Build a $set-style update payload from a data dict."""
    return {f"{k}": v for k, v in data.items() if v is not None}
