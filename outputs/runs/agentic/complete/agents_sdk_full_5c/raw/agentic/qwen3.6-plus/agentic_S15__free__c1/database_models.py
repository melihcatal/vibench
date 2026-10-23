"""
database_models.py - Local request, response, and normalization helpers
for Managed NoSQL Document Store (MongoDB Atlas).
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRecord:
    """Canonical representation of a document in the store."""
    doc_id: str
    data: Dict[str, Any]
    partition_key: Optional[str] = None
    version: int = 1
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_mongo(self) -> Dict[str, Any]:
        """Serialize to a MongoDB-compatible document."""
        doc = {
            "_id": self.doc_id,
            "data": self.data,
            "version": self.version,
            "metadata": self.metadata,
        }
        if self.partition_key:
            doc["partition_key"] = self.partition_key
        if self.created_at:
            doc["created_at"] = self.created_at
        if self.updated_at:
            doc["updated_at"] = self.updated_at
        return doc

    @classmethod
    def from_mongo(cls, raw: Dict[str, Any]) -> "DocumentRecord":
        """Deserialize from a raw MongoDB document."""
        return cls(
            doc_id=raw.get("_id", ""),
            data=raw.get("data", {}),
            partition_key=raw.get("partition_key"),
            version=raw.get("version", 1),
            created_at=raw.get("created_at"),
            updated_at=raw.get("updated_at"),
            metadata=raw.get("metadata", {}),
        )


@dataclass
class UpsertRequest:
    """Request payload for upserting a document."""
    doc_id: str
    data: Dict[str, Any]
    partition_key: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class QueryRequest:
    """Request payload for querying documents."""
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None
    limit: int = 50


@dataclass
class ConditionalUpdateRequest:
    """Request for a version-aware or conditional update."""
    doc_id: str
    updates: Dict[str, Any]
    expected_version: Optional[int] = None
    condition_field: Optional[str] = None
    condition_value: Any = None


@dataclass
class FetchResponse:
    """Response wrapper for a fetched document."""
    found: bool
    document: Optional[DocumentRecord] = None
    error: Optional[str] = None


@dataclass
class QueryResponse:
    """Response wrapper for a query result set."""
    documents: List[DocumentRecord] = field(default_factory=list)
    count: int = 0
    error: Optional[str] = None


def now_utc_iso() -> str:
    """Return current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


def normalize_user_content(content: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize and normalize user-supplied document content
    before storage in MongoDB Atlas.
    """
    cleaned = {}
    for key, value in content.items():
        if isinstance(value, str):
            cleaned[key] = value.strip()
        elif isinstance(value, (dict, list)):
            cleaned[key] = value
        elif value is None:
            continue
        else:
            cleaned[key] = str(value)
    return cleaned


def extract_user_facing_fields(document: DocumentRecord) -> Dict[str, str]:
    """
    Extract text fields that may contain user-generated content
    suitable for downstream processing (translation, safety checks, summary).
    """
    fields = {}
    data = document.data or {}
    for key in ("title", "description", "body", "content", "notes", "comment"):
        val = data.get(key)
        if isinstance(val, str) and val.strip():
            fields[key] = val.strip()
    return fields
