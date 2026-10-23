from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, asdict
import json


@dataclass
class DocumentRequest:
    """Request model for document operations."""

    collection_name: str
    document_id: str
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "collection_name": self.collection_name,
            "document_id": self.document_id,
            "data": self.data,
        }
        if self.metadata:
            result["metadata"] = self.metadata
        return result

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


@dataclass
class DocumentResponse:
    """Response model for document operations."""

    success: bool
    document_id: str
    action: str
    timestamp: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "success": self.success,
            "document_id": self.document_id,
            "action": self.action,
            "timestamp": self.timestamp,
        }
        if self.data:
            result["data"] = self.data
        if self.error:
            result["error"] = self.error
        if self.metadata:
            result["metadata"] = self.metadata
        return result

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


@dataclass
class QueryRequest:
    """Request model for document queries."""

    collection_name: str
    field_name: Optional[str] = None
    field_value: Optional[Any] = None
    partition_key: Optional[str] = None
    limit: int = 100
    filters: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {"collection_name": self.collection_name, "limit": self.limit}
        if self.field_name and self.field_value is not None:
            result["field_name"] = self.field_name
            result["field_value"] = self.field_value
        if self.partition_key:
            result["partition_key"] = self.partition_key
        if self.filters:
            result["filters"] = self.filters
        return result


@dataclass
class QueryResponse:
    """Response model for document queries."""

    success: bool
    collection_name: str
    documents: List[Dict[str, Any]]
    count: int
    timestamp: str
    query_params: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "success": self.success,
            "collection_name": self.collection_name,
            "documents": self.documents,
            "count": self.count,
            "timestamp": self.timestamp,
        }
        if self.query_params:
            result["query_params"] = self.query_params
        if self.error:
            result["error"] = self.error
        return result


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize MongoDB document for API response.

    Args:
        document: Raw MongoDB document

    Returns:
        dict: Normalized document
    """
    if not document:
        return {}

    normalized = dict(document)

    if "_id" in normalized:
        normalized["id"] = str(normalized["_id"])
        del normalized["_id"]

    return normalized


def prepare_document_for_storage(
    data: Dict[str, Any], document_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Prepare document data for MongoDB storage.

    Args:
        data: Document data
        document_id: Optional document ID

    Returns:
        dict: Prepared document
    """
    prepared = dict(data)

    if document_id:
        prepared["_id"] = document_id

    if "timestamp" not in prepared:
        prepared["timestamp"] = datetime.utcnow().isoformat()

    return prepared


def validate_document_schema(
    data: Dict[str, Any], required_fields: List[str] = None
) -> bool:
    """
    Validate document schema.

    Args:
        data: Document data
        required_fields: List of required field names

    Returns:
        bool: True if valid
    """
    if not isinstance(data, dict):
        return False

    if required_fields:
        for field in required_fields:
            if field not in data:
                return False

    return True
