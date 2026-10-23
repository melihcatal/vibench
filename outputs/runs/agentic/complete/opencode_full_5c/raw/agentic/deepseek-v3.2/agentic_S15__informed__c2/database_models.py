from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import json
from bson import ObjectId


@dataclass
class DocumentRequest:
    """Request model for document operations."""

    collection_name: str
    document_id: Union[str, ObjectId]
    document_data: Dict[str, Any]
    options: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        if isinstance(result["document_id"], ObjectId):
            result["document_id"] = str(result["document_id"])
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentRequest":
        """Create from dictionary."""
        doc_id = data.get("document_id")
        if isinstance(doc_id, str) and ObjectId.is_valid(doc_id):
            data["document_id"] = ObjectId(doc_id)
        return cls(**data)


@dataclass
class QueryRequest:
    """Request model for query operations."""

    collection_name: str
    field_name: Optional[str] = None
    field_value: Optional[Any] = None
    partition_key: Optional[str] = None
    limit: int = 100
    filters: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QueryRequest":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class ConditionalUpdateRequest:
    """Request model for conditional update operations."""

    collection_name: str
    document_id: Union[str, ObjectId]
    update_data: Dict[str, Any]
    condition_field: Optional[str] = None
    condition_value: Optional[Any] = None
    version_field: str = "_version"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        if isinstance(result["document_id"], ObjectId):
            result["document_id"] = str(result["document_id"])
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConditionalUpdateRequest":
        """Create from dictionary."""
        doc_id = data.get("document_id")
        if isinstance(doc_id, str) and ObjectId.is_valid(doc_id):
            data["document_id"] = ObjectId(doc_id)
        return cls(**data)


@dataclass
class DocumentResponse:
    """Response model for document operations."""

    success: bool
    document_id: Union[str, ObjectId]
    operation: Optional[str] = None
    document: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        if isinstance(result["document_id"], ObjectId):
            result["document_id"] = str(result["document_id"])

        # Convert document if it contains ObjectId
        if result["document"]:
            result["document"] = convert_objectids(result["document"])

        return result

    @classmethod
    def success_response(
        cls,
        document_id: Union[str, ObjectId],
        operation: str = None,
        document: Dict[str, Any] = None,
        metadata: Dict[str, Any] = None,
    ) -> "DocumentResponse":
        """Create success response."""
        return cls(
            success=True,
            document_id=document_id,
            operation=operation,
            document=document,
            metadata=metadata or {},
        )

    @classmethod
    def error_response(
        cls, document_id: Union[str, ObjectId], error: str, operation: str = None
    ) -> "DocumentResponse":
        """Create error response."""
        return cls(
            success=False, document_id=document_id, operation=operation, error=error
        )


@dataclass
class QueryResponse:
    """Response model for query operations."""

    success: bool
    documents: List[Dict[str, Any]]
    count: int
    query: Dict[str, Any]
    limit: int
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        result["documents"] = convert_objectids(result["documents"])
        return result

    @classmethod
    def success_response(
        cls, documents: List[Dict[str, Any]], query: Dict[str, Any], limit: int
    ) -> "QueryResponse":
        """Create success response."""
        return cls(
            success=True,
            documents=documents,
            count=len(documents),
            query=query,
            limit=limit,
        )

    @classmethod
    def error_response(cls, error: str, query: Dict[str, Any]) -> "QueryResponse":
        """Create error response."""
        return cls(
            success=False, documents=[], count=0, query=query, limit=0, error=error
        )


def convert_objectids(data: Any) -> Any:
    """
    Convert ObjectId instances to strings in nested data structures.

    Args:
        data: Data structure possibly containing ObjectIds

    Returns:
        Data with ObjectIds converted to strings
    """
    from bson import ObjectId

    if isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, dict):
        return {k: convert_objectids(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectids(item) for item in data]
    else:
        return data


def create_document_metadata(
    created_by: str = None, tags: List[str] = None
) -> Dict[str, Any]:
    """
    Create standard metadata for documents.

    Args:
        created_by: User or system that created the document
        tags: List of tags for the document

    Returns:
        Metadata dictionary
    """
    metadata = {
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "_version": 1,
    }

    if created_by:
        metadata["created_by"] = created_by

    if tags:
        metadata["tags"] = tags

    return metadata


def update_document_metadata(
    existing_metadata: Dict[str, Any], updated_by: str = None
) -> Dict[str, Any]:
    """
    Update document metadata.

    Args:
        existing_metadata: Existing metadata dictionary
        updated_by: User or system that updated the document

    Returns:
        Updated metadata
    """
    metadata = existing_metadata.copy()
    metadata["updated_at"] = datetime.utcnow().isoformat()

    if "_version" in metadata:
        metadata["_version"] += 1

    if updated_by:
        metadata["updated_by"] = updated_by

    return metadata
