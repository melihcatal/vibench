from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class DocumentRequest(BaseModel):
    """
    Standardized request model for document operations.
    """
    document_id: str = Field(..., description="Primary identifier of the document")
    partition_key: str = Field(..., description="Partition key for the document")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Document payload")

class DocumentResponse(BaseModel):
    """
    Standardized response model for document operations.
    """
    document_id: str
    partition_key: str
    payload: Dict[str, Any]
    etag: Optional[str] = Field(None, description="ETag for optimistic concurrency control")

def normalize_document(raw_document: Dict[str, Any]) -> DocumentResponse:
    """
    Normalizes a raw document from Azure Cosmos DB into a standardized response.
    """
    return DocumentResponse(
        document_id=raw_document["id"],
        partition_key=raw_document.get("partitionKey", raw_document["id"]),
        payload={k: v for k, v in raw_document.items() if k not in ["id", "_rid", "_self", "_etag", "_attachments", "_ts"]},
        etag=raw_document.get("_etag")
    )