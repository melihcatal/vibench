"""
Local helper: database_models.py
Define local request, response, and normalization helpers for Managed NoSQL Document Store.
Designed to work with MongoDB Atlas document structures.
"""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from datetime import datetime


@dataclass
class DocumentRequest:
    """Request model for document operations."""
    document_id: str
    data: Dict[str, Any]
    partition_key: Optional[str] = None
    version: Optional[int] = None

    def to_mongo_doc(self) -> Dict[str, Any]:
        """Convert to a MongoDB-compatible document dict."""
        doc = {
            "_id": self.document_id,
            "data": self.data,
            "updated_at": datetime.utcnow().isoformat(),
        }
        if self.partition_key is not None:
            doc["partition_key"] = self.partition_key
        if self.version is not None:
            doc["version"] = self.version
        return doc


@dataclass
class DocumentResponse:
    """Response model wrapping a retrieved document."""
    document_id: str
    data: Dict[str, Any]
    partition_key: Optional[str] = None
    version: Optional[int] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_mongo_doc(cls, doc: Dict[str, Any]) -> "DocumentResponse":
        """Construct from a raw MongoDB document."""
        return cls(
            document_id=doc.get("_id", ""),
            data=doc.get("data", {}),
            partition_key=doc.get("partition_key"),
            version=doc.get("version"),
            updated_at=doc.get("updated_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a plain dictionary."""
        return asdict(self)


@dataclass
class QueryResult:
    """Container for a batch of queried documents."""
    documents: List[DocumentResponse] = field(default_factory=list)
    total_count: int = 0

    def to_list(self) -> List[Dict[str, Any]]:
        """Return all documents as a list of dictionaries."""
        return [doc.to_dict() for doc in self.documents]


def normalize_field_value(value: Any) -> Any:
    """
    Normalize a field value for storage in MongoDB Atlas.
    Handles basic type coercion and sanitization.
    """
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        return {k: normalize_field_value(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [normalize_field_value(item) for item in value if item is not None]
    return value


def build_partition_query(partition_key: str, partition_value: str) -> Dict[str, Any]:
    """
    Build a MongoDB query dict for partition-key style filtering.
    """
    return {"partition_key": partition_value} if partition_key else {}
