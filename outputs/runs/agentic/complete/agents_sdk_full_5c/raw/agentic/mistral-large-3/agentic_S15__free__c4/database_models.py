from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class DocumentRequest(BaseModel):
    """Request model for document operations."""
    id: str = Field(..., description="Primary identifier of the document.")
    partition_key: Optional[str] = Field(None, description="Partition key for the document.")
    payload: Dict[str, Any] = Field(..., description="Document content.")

class DocumentResponse(BaseModel):
    """Response model for document operations."""
    id: str
    partition_key: Optional[str]
    payload: Dict[str, Any]
    etag: Optional[str] = Field(None, description="ETag for optimistic concurrency control.")

def normalize_document(document: Dict[str, Any]) -> DocumentResponse:
    """Normalizes a raw document response into a structured model."""
    return DocumentResponse(
        id=document.get("id"),
        partition_key=document.get("partition_key"),
        payload=document,
        etag=document.get("_etag")
    )