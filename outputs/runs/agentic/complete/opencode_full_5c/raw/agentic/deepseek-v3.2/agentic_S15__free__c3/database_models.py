from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class DocumentRequest:
    """Request model for document operations."""

    id: str
    data: Dict[str, Any]
    collection: Optional[str] = None
    version: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {"id": self.id, "data": self.data}
        if self.collection:
            result["collection"] = self.collection
        if self.version is not None:
            result["version"] = self.version
        return result

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


@dataclass
class DocumentResponse:
    """Response model for document operations."""

    success: bool
    document_id: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    version: Optional[int] = None
    updated_at: Optional[str] = None
    provider: str = "aws:dynamodb"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "success": self.success,
            "document_id": self.document_id,
            "provider": self.provider,
        }
        if self.data is not None:
            result["data"] = self.data
        if self.error:
            result["error"] = self.error
        if self.version is not None:
            result["version"] = self.version
        if self.updated_at:
            result["updated_at"] = self.updated_at
        return result


@dataclass
class QueryRequest:
    """Request model for query operations."""

    field_name: str
    field_value: Any
    collection: Optional[str] = None
    limit: int = 100

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "field_name": self.field_name,
            "field_value": self.field_value,
            "limit": self.limit,
        }
        if self.collection:
            result["collection"] = self.collection
        return result


@dataclass
class QueryResponse:
    """Response model for query operations."""

    success: bool
    documents: List[Dict[str, Any]]
    count: int
    field_name: str
    field_value: Any
    error: Optional[str] = None
    provider: str = "aws:dynamodb"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "success": self.success,
            "documents": self.documents,
            "count": self.count,
            "field_name": self.field_name,
            "field_value": self.field_value,
            "provider": self.provider,
        }
        if self.error:
            result["error"] = self.error
        return result


@dataclass
class ConditionalUpdateRequest:
    """Request model for conditional update operations."""

    document_id: str
    updates: Dict[str, Any]
    collection: Optional[str] = None
    condition_field: Optional[str] = None
    condition_value: Optional[Any] = None
    expected_version: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {"document_id": self.document_id, "updates": self.updates}
        if self.collection:
            result["collection"] = self.collection
        if self.condition_field:
            result["condition_field"] = self.condition_field
        if self.condition_value is not None:
            result["condition_value"] = self.condition_value
        if self.expected_version is not None:
            result["expected_version"] = self.expected_version
        return result


@dataclass
class ConditionalUpdateResponse:
    """Response model for conditional update operations."""

    success: bool
    document_id: str
    updated_data: Optional[Dict[str, Any]] = None
    previous_version: Optional[int] = None
    new_version: Optional[int] = None
    error: Optional[str] = None
    provider: str = "aws:dynamodb"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "success": self.success,
            "document_id": self.document_id,
            "provider": self.provider,
        }
        if self.updated_data is not None:
            result["updated_data"] = self.updated_data
        if self.previous_version is not None:
            result["previous_version"] = self.previous_version
        if self.new_version is not None:
            result["new_version"] = self.new_version
        if self.error:
            result["error"] = self.error
        return result


class DocumentNormalizer:
    """Helper class for normalizing document data."""

    @staticmethod
    def add_metadata(document: Dict[str, Any], is_new: bool = True) -> Dict[str, Any]:
        """
        Add metadata to document.

        Args:
            document: Original document
            is_new: Whether this is a new document

        Returns:
            Document with metadata
        """
        normalized = document.copy()
        timestamp = datetime.utcnow().isoformat() + "Z"

        if is_new:
            normalized["_created_at"] = timestamp
            normalized["_version"] = 1
        else:
            if "_created_at" not in normalized:
                normalized["_created_at"] = timestamp

        normalized["_updated_at"] = timestamp

        if "_version" in normalized:
            normalized["_version"] += 1
        else:
            normalized["_version"] = 1

        return normalized

    @staticmethod
    def extract_user_fields(document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract user-facing fields from document.

        Args:
            document: Full document with metadata

        Returns:
            User-facing fields only
        """
        user_fields = {}
        for key, value in document.items():
            if not key.startswith("_"):
                user_fields[key] = value
        return user_fields

    @staticmethod
    def validate_document_structure(document: Dict[str, Any]) -> List[str]:
        """
        Validate document structure.

        Args:
            document: Document to validate

        Returns:
            List of validation errors
        """
        errors = []

        # Check for required fields
        if not document:
            errors.append("Document cannot be empty")

        # Check size limit (approx 400KB for DynamoDB item limit)
        document_size = len(json.dumps(document).encode("utf-8"))
        if document_size > 400 * 1024:  # 400KB
            errors.append(f"Document too large: {document_size} bytes (max 400KB)")

        return errors


class ResponseBuilder:
    """Helper class for building standardized responses."""

    @staticmethod
    def success(
        document_id: str, data: Optional[Dict[str, Any]] = None, **kwargs
    ) -> DocumentResponse:
        """Build success response."""
        return DocumentResponse(
            success=True, document_id=document_id, data=data, **kwargs
        )

    @staticmethod
    def error(document_id: str, error_message: str, **kwargs) -> DocumentResponse:
        """Build error response."""
        return DocumentResponse(
            success=False, document_id=document_id, error=error_message, **kwargs
        )

    @staticmethod
    def query_success(
        documents: List[Dict[str, Any]], field_name: str, field_value: Any, **kwargs
    ) -> QueryResponse:
        """Build query success response."""
        return QueryResponse(
            success=True,
            documents=documents,
            count=len(documents),
            field_name=field_name,
            field_value=field_value,
            **kwargs,
        )

    @staticmethod
    def query_error(
        field_name: str, field_value: Any, error_message: str, **kwargs
    ) -> QueryResponse:
        """Build query error response."""
        return QueryResponse(
            success=False,
            documents=[],
            count=0,
            field_name=field_name,
            field_value=field_value,
            error=error_message,
            **kwargs,
        )
