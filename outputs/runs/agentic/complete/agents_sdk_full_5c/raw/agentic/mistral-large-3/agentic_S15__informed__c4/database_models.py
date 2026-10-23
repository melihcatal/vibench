from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class DocumentRequest(BaseModel):
    """Request model for document upsert and fetch operations."""
    document_id: str = Field(..., description="Primary identifier for the document.")
    payload: Dict[str, Any] = Field(..., description="Document content as a JSON-serializable dictionary.")
    partition_key: Optional[str] = Field(None, description="Optional partition key for the document.")


class DocumentResponse(BaseModel):
    """Response model for document fetch and query operations."""
    document_id: str
    payload: Dict[str, Any]
    version: Optional[int] = Field(None, description="Document version or revision number.")


class QueryRequest(BaseModel):
    """Request model for querying documents by field value."""
    field_name: str = Field(..., description="Field name to query by.")
    field_value: Any = Field(..., description="Field value to match.")
    partition_key: Optional[str] = Field(None, description="Optional partition key for the query.")


def normalize_document(document: Dict[str, Any]) -> DocumentResponse:
    """Normalize a raw MongoDB document into a DocumentResponse."""
    return DocumentResponse(
        document_id=str(document.get("_id")),
        payload={k: v for k, v in document.items() if k != "_id"},
        version=document.get("version")
    )