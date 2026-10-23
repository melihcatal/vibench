from typing import Dict, Any, Optional, List
from datetime import datetime
import json


class DocumentRequest:
    """Request model for document operations."""

    def __init__(self, collection_name: str, document_id: str, data: Dict[str, Any]):
        self.collection_name = collection_name
        self.document_id = document_id
        self.data = data
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary."""
        return {
            "collection_name": self.collection_name,
            "document_id": self.document_id,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentRequest":
        """Create request from dictionary."""
        return cls(
            collection_name=data["collection_name"],
            document_id=data["document_id"],
            data=data["data"],
        )


class DocumentResponse:
    """Response model for document operations."""

    def __init__(
        self,
        success: bool,
        document_id: str,
        document: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.success = success
        self.document_id = document_id
        self.document = document
        self.error = error
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        result = {
            "success": self.success,
            "document_id": self.document_id,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

        if self.document:
            result["document"] = self.document
        if self.error:
            result["error"] = self.error

        return result

    @classmethod
    def from_mongodb_result(
        cls, document_id: str, mongodb_result: Dict[str, Any]
    ) -> "DocumentResponse":
        """Create response from MongoDB result."""
        success = mongodb_result.get("success", False)
        error = mongodb_result.get("error")
        document = mongodb_result.get("document")

        # Extract metadata
        metadata = {
            k: v
            for k, v in mongodb_result.items()
            if k not in ["success", "document_id", "document", "error", "timestamp"]
        }

        return cls(
            success=success,
            document_id=document_id,
            document=document,
            error=error,
            metadata=metadata,
        )


class QueryRequest:
    """Request model for query operations."""

    def __init__(
        self, collection_name: str, field_name: str, field_value: Any, limit: int = 100
    ):
        self.collection_name = collection_name
        self.field_name = field_name
        self.field_value = field_value
        self.limit = limit
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary."""
        return {
            "collection_name": self.collection_name,
            "field_name": self.field_name,
            "field_value": self.field_value,
            "limit": self.limit,
            "timestamp": self.timestamp.isoformat(),
        }


class QueryResponse:
    """Response model for query operations."""

    def __init__(
        self,
        success: bool,
        documents: List[Dict[str, Any]],
        count: int,
        field_name: str,
        field_value: Any,
        error: Optional[str] = None,
    ):
        self.success = success
        self.documents = documents
        self.count = count
        self.field_name = field_name
        self.field_value = field_value
        self.error = error
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        result = {
            "success": self.success,
            "documents": self.documents,
            "count": self.count,
            "field_name": self.field_name,
            "field_value": self.field_value,
            "timestamp": self.timestamp.isoformat(),
        }

        if self.error:
            result["error"] = self.error

        return result


class ConditionalUpdateRequest:
    """Request model for conditional update operations."""

    def __init__(
        self,
        collection_name: str,
        document_id: str,
        update_data: Dict[str, Any],
        condition_field: str,
        condition_value: Any,
    ):
        self.collection_name = collection_name
        self.document_id = document_id
        self.update_data = update_data
        self.condition_field = condition_field
        self.condition_value = condition_value
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary."""
        return {
            "collection_name": self.collection_name,
            "document_id": self.document_id,
            "update_data": self.update_data,
            "condition_field": self.condition_field,
            "condition_value": self.condition_value,
            "timestamp": self.timestamp.isoformat(),
        }


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize MongoDB document for JSON serialization.

    Args:
        document: MongoDB document

    Returns:
        dict: Normalized document
    """
    if not document:
        return {}

    normalized = document.copy()

    # Convert ObjectId to string
    if "_id" in normalized:
        normalized["_id"] = str(normalized["_id"])

    # Convert datetime objects to ISO format strings
    for key, value in normalized.items():
        if isinstance(value, datetime):
            normalized[key] = value.isoformat()

    return normalized


def validate_document_schema(
    document: Dict[str, Any], required_fields: List[str] = None
) -> bool:
    """
    Validate document schema.

    Args:
        document: Document to validate
        required_fields: List of required field names

    Returns:
        bool: True if valid
    """
    if not isinstance(document, dict):
        return False

    if required_fields:
        for field in required_fields:
            if field not in document:
                return False

    return True
