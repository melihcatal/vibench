"""
Local request, response, and normalization helpers for MongoDB Atlas managed NoSQL document store.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class DocumentRecord:
    """Normalized representation of a document stored in MongoDB Atlas."""
    doc_id: str
    content: dict[str, Any]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: Optional[str] = None
    version: int = 1
    partition_key: Optional[str] = None

    def to_mongo_insert(self) -> dict[str, Any]:
        """Convert to a MongoDB Atlas insert payload with _id and metadata fields."""
        payload = {
            "_id": self.doc_id,
            "data": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at or self.created_at,
            "version": self.version,
        }
        if self.partition_key:
            payload["partition_key"] = self.partition_key
        return payload

    def to_mongo_update(self) -> dict[str, Any]:
        """Convert to a MongoDB Atlas update payload ($set fields)."""
        return {
            "$set": {
                "data": self.content,
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "version": self.version,
            }
        }

    @classmethod
    def from_mongo_document(cls, doc: dict[str, Any]) -> DocumentRecord:
        """Reconstruct a DocumentRecord from a MongoDB Atlas query result."""
        return cls(
            doc_id=doc.get("_id", str(uuid.uuid4())),
            content=doc.get("data", {}),
            created_at=doc.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=doc.get("updated_at"),
            version=doc.get("version", 1),
            partition_key=doc.get("partition_key"),
        )


@dataclass
class QueryFilter:
    """Normalized query filter for MongoDB Atlas document queries."""
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None
    exact_match: bool = True

    def to_mongo_filter(self) -> dict[str, Any]:
        """Convert to a MongoDB Atlas query filter dictionary."""
        mongo_filter: dict[str, Any] = {}
        if self.exact_match:
            mongo_filter[f"data.{self.field_name}"] = self.field_value
        else:
            mongo_filter[f"data.{self.field_name}"] = {"$regex": str(self.field_value), "$options": "i"}
        if self.partition_key:
            mongo_filter["partition_key"] = self.partition_key
        return mongo_filter


@dataclass
class ConditionalUpdateSpec:
    """Specification for a conditional, version-aware update on MongoDB Atlas."""
    doc_id: str
    updates: dict[str, Any]
    expected_version: Optional[int] = None
    required_field: Optional[str] = None
    required_field_value: Optional[Any] = None

    def to_mongo_update_filter(self) -> dict[str, Any]:
        """Build the MongoDB Atlas filter for a conditional update."""
        mongo_filter: dict[str, Any] = {"_id": self.doc_id}
        if self.expected_version is not None:
            mongo_filter["version"] = self.expected_version
        if self.required_field is not None:
            field_path = f"data.{self.required_field}"
            if self.required_field_value is not None:
                mongo_filter[field_path] = self.required_field_value
            else:
                mongo_filter[field_path] = {"$exists": True}
        return mongo_filter

    def to_mongo_update_payload(self) -> dict[str, Any]:
        """Build the MongoDB Atlas $set update payload with version increment."""
        return {
            "$set": {
                "data": self.updates,
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "version": self.expected_version + 1 if self.expected_version is not None else 2,
            }
        }


@dataclass
class QueryResponse:
    """Normalized response wrapper for MongoDB Atlas query results."""
    documents: list[DocumentRecord] = field(default_factory=list)
    total_count: int = 0
    query_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "documents": [asdict(d) for d in self.documents],
            "total_count": self.total_count,
            "query_timestamp": self.query_timestamp,
        }


def normalize_document_id(raw_id: Any) -> str:
    """Normalize a document identifier to a string suitable for MongoDB Atlas _id."""
    if isinstance(raw_id, str):
        return raw_id
    return str(raw_id)


def sanitize_for_mongo(value: Any) -> Any:
    """
    Recursively sanitize a value for MongoDB Atlas storage.
    Removes or converts types that are not BSON-compatible.
    """
    if isinstance(value, dict):
        sanitized = {}
        for k, v in value.items():
            clean_key = str(k).replace(".", "_")
            sanitized[clean_key] = sanitize_for_mongo(v)
        return sanitized
    elif isinstance(value, list):
        return [sanitize_for_mongo(item) for item in value]
    elif isinstance(value, datetime):
        return value.isoformat()
    return value
