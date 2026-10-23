from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class DocumentRequest:
    """Request model for document operations."""

    collection: str
    document_id: str
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        return result


@dataclass
class DocumentResponse:
    """Response model for document operations."""

    success: bool
    document_id: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        return result


@dataclass
class QueryRequest:
    """Request model for query operations."""

    collection: str
    filters: Dict[str, Any]
    limit: int = 100
    skip: int = 0
    sort: Optional[List[tuple]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        return result


@dataclass
class QueryResponse:
    """Response model for query operations."""

    success: bool
    documents: List[Dict[str, Any]]
    count: int
    error: Optional[str] = None
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        return result


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize document for storage.

    Args:
        document: Raw document data

    Returns:
        Normalized document
    """
    normalized = document.copy()

    # Ensure timestamp fields are strings
    for key, value in document.items():
        if isinstance(value, datetime):
            normalized[key] = value.isoformat()

    return normalized


def parse_document_response(mongodb_result: Dict[str, Any]) -> DocumentResponse:
    """
    Parse MongoDB result into DocumentResponse.

    Args:
        mongodb_result: Result from MongoDB operation

    Returns:
        DocumentResponse
    """
    if "error" in mongodb_result:
        return DocumentResponse(
            success=False,
            document_id=mongodb_result.get("document_id", ""),
            error=mongodb_result["error"],
        )

    return DocumentResponse(
        success=True,
        document_id=mongodb_result.get("document_id", ""),
        data=mongodb_result.get("data"),
    )


def create_metadata(author: str, tags: List[str] = None) -> Dict[str, Any]:
    """
    Create standard metadata for documents.

    Args:
        author: Document author
        tags: List of tags

    Returns:
        Metadata dictionary
    """
    metadata = {
        "created_at": datetime.utcnow().isoformat(),
        "author": author,
        "version": 1,
    }

    if tags:
        metadata["tags"] = tags

    return metadata
