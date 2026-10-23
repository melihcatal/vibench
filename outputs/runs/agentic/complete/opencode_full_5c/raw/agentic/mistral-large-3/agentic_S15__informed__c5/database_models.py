from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    """
    Standardized request model for document operations.
    """

    document_id: str = Field(..., description="Primary identifier of the document")
    partition_key: Optional[str] = Field(None, description="Partition key value")
    document: Optional[Dict[str, Any]] = Field(None, description="Document content")


class DocumentResponse(BaseModel):
    """
    Standardized response model for document operations.
    """

    document_id: str = Field(..., description="Primary identifier of the document")
    document: Dict[str, Any] = Field(..., description="Document content")
    etag: Optional[str] = Field(None, description="ETag for versioning")
    timestamp: Optional[str] = Field(None, description="Last updated timestamp")


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a document for storage in Azure Cosmos DB.

    Args:
        document: Input document

    Returns:
        Normalized document
    """
    normalized = document.copy()
    if "id" not in normalized:
        raise ValueError("Document must contain an 'id' field")
    return normalized


def parse_query_response(items: List[Dict[str, Any]]) -> List[DocumentResponse]:
    """
    Parses query results into standardized response models.

    Args:
        items: List of raw query results

    Returns:
        List of standardized document responses
    """
    return [
        DocumentResponse(
            document_id=item["id"],
            document=item,
            etag=item.get("_etag"),
            timestamp=item.get("_ts"),
        )
        for item in items
    ]
