from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    """Request model for document operations." ""
    document_id: str = Field(..., description="The primary identifier of the document.")
    document: Dict[str, Any] = Field(..., description="The JSON document to upsert or update.")
    partition_key: str = Field("id", description="The partition key attribute name.")


class DocumentResponse(BaseModel):
    """Response model for document operations." ""
    document: Dict[str, Any] = Field(..., description="The fetched or updated document.")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata from the operation.")


class QueryRequest(BaseModel):
    """Request model for querying documents." ""
    field_name: str = Field(..., description="The name of the field to query.")
    field_value: Any = Field(..., description="The value of the field to match.")
    index_name: Optional[str] = Field(None, description="The name of the secondary index to use.")


class QueryResponse(BaseModel):
    """Response model for querying documents." ""
    documents: List[Dict[str, Any]] = Field(..., description="The list of matching documents.")


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes a document for storage or response." ""
    return {k: v for k, v in document.items() if v is not None}