from typing import Any, Dict, Optional, TypedDict
from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_id: str = Field(..., alias="id")
    partition_key: Optional[str] = None
    body: Dict[str, Any]

    class Config:
        populate_by_name = True


class DocumentResponse(TypedDict):
    id: str
    partition_key: Optional[str]
    body: Dict[str, Any]
    etag: Optional[str]
    last_modified: Optional[str]


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize document structure for Azure Cosmos DB."""
    normalized = {"id": document.get("id", document.get("document_id"))}
    normalized.update(document.get("body", {}))
    return normalized
