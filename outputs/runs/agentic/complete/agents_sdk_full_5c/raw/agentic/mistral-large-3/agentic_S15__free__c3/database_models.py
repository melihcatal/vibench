from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class DocumentRequest(BaseModel):
    """Request model for document operations."""
    document_id: str = Field(..., description="The unique identifier of the document.")
    partition_key: str = Field(..., description="The partition key for the document.")
    data: Dict[str, Any] = Field(default_factory=dict, description="The document data.")


class DocumentResponse(BaseModel):
    """Response model for document operations."""
    document_id: str = Field(..., description="The unique identifier of the document.")
    partition_key: str = Field(..., description="The partition key for the document.")
    data: Dict[str, Any] = Field(..., description="The document data.")
    etag: Optional[str] = Field(None, description="The entity tag for concurrency control.")
    timestamp: Optional[int] = Field(None, description="The last updated timestamp.")


def normalize_document(raw_document: Dict[str, Any]) -> DocumentResponse:
    """
    Normalizes a raw document from Cosmos DB into a structured response.
    
    Args:
        raw_document: The raw document from Cosmos DB.
        
    Returns:
        A normalized DocumentResponse object.
    """
    return DocumentResponse(
        document_id=raw_document.get("id", ""),
        partition_key=raw_document.get("partitionKey", ""),
        data=raw_document,
        etag=raw_document.get("_etag"),
        timestamp=raw_document.get("_ts")
    )