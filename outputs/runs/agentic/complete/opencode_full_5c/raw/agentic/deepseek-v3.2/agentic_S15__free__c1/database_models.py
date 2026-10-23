from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import uuid


@dataclass
class DocumentRequest:
    """Request model for document operations."""

    id: str
    data: Dict[str, Any]
    collection: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        result = {"id": self.id, "data": self.data}

        if self.metadata:
            result["metadata"] = self.metadata

        return result

    def to_dynamodb_item(self) -> Dict[str, Any]:
        """Convert to DynamoDB item format."""
        item = {
            "id": self.id,
            "data": json.dumps(self.data),
            "updated_at": datetime.utcnow().isoformat() + "Z",
        }

        if self.metadata:
            item["metadata"] = json.dumps(self.metadata)

        return item

    @classmethod
    def from_dynamodb_item(cls, item: Dict[str, Any]) -> "DocumentRequest":
        """Create from DynamoDB item."""
        try:
            data = json.loads(item.get("data", "{}"))
        except json.JSONDecodeError:
            data = {}

        try:
            metadata = json.loads(item.get("metadata", "{}"))
        except (json.JSONDecodeError, KeyError):
            metadata = {}

        return cls(id=item.get("id", ""), data=data, metadata=metadata)


@dataclass
class DocumentResponse:
    """Response model for document operations."""

    success: bool
    document_id: str
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    provider: Optional[str] = None
    operation: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {"success": self.success, "document_id": self.document_id}

        if self.data:
            result["data"] = self.data

        if self.metadata:
            result["metadata"] = self.metadata

        if self.error:
            result["error"] = self.error

        if self.provider:
            result["provider"] = self.provider

        if self.operation:
            result["operation"] = self.operation

        return result


@dataclass
class QueryRequest:
    """Request model for document queries."""

    field_name: str
    field_value: Any
    collection: Optional[str] = None
    limit: int = 100
    offset: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "field_name": self.field_name,
            "field_value": self.field_value,
            "limit": self.limit,
            "offset": self.offset,
        }


@dataclass
class QueryResponse:
    """Response model for document queries."""

    success: bool
    documents: List[Dict[str, Any]]
    count: int
    query: Dict[str, Any]
    provider: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "success": self.success,
            "documents": self.documents,
            "count": self.count,
            "query": self.query,
        }

        if self.provider:
            result["provider"] = self.provider

        if self.error:
            result["error"] = self.error

        return result


@dataclass
class ConditionalUpdateRequest:
    """Request model for conditional updates."""

    document_id: str
    updates: Dict[str, Any]
    condition_field: Optional[str] = None
    condition_value: Optional[Any] = None
    collection: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {"document_id": self.document_id, "updates": self.updates}

        if self.condition_field:
            result["condition_field"] = self.condition_field

        if self.condition_value is not None:
            result["condition_value"] = self.condition_value

        return result


@dataclass
class ConditionalUpdateResponse:
    """Response model for conditional updates."""

    success: bool
    document_id: str
    updated_fields: List[str]
    new_version: Optional[int] = None
    condition_checked: bool = False
    provider: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "success": self.success,
            "document_id": self.document_id,
            "updated_fields": self.updated_fields,
            "condition_checked": self.condition_checked,
        }

        if self.new_version is not None:
            result["new_version"] = self.new_version

        if self.provider:
            result["provider"] = self.provider

        if self.error:
            result["error"] = self.error

        return result


def normalize_document_data(data: Any) -> Dict[str, Any]:
    """Normalize document data to ensure it's a dictionary."""
    if isinstance(data, dict):
        return data
    elif isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return {"content": data}
    elif data is None:
        return {}
    else:
        # Try to convert to dict
        try:
            return dict(data)
        except (TypeError, ValueError):
            return {"value": str(data)}


def generate_document_id(prefix: str = "doc") -> str:
    """Generate a unique document ID."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def extract_metadata_from_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """Extract metadata from document data."""
    metadata = {
        "size": len(json.dumps(document).encode("utf-8")),
        "fields_count": len(document),
        "field_names": list(document.keys()),
    }

    # Add type information for each field
    field_types = {}
    for key, value in document.items():
        field_types[key] = type(value).__name__

    metadata["field_types"] = field_types

    return metadata


def validate_document_structure(
    document: Dict[str, Any], required_fields: List[str] = None
) -> Dict[str, Any]:
    """Validate document structure and return validation result."""
    if required_fields is None:
        required_fields = []

    missing_fields = [field for field in required_fields if field not in document]

    validation_result = {
        "valid": len(missing_fields) == 0,
        "missing_fields": missing_fields,
        "total_fields": len(document),
        "has_id": "id" in document,
    }

    return validation_result
