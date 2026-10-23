from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    """
    A model for standardizing document request payloads.
    """

    db_name: str
    doc_id: Optional[str] = None
    document: Optional[Dict[str, Any]] = None
    revision: Optional[str] = None


class DocumentResponse(BaseModel):
    """
    A model for standardizing document response payloads.
    """

    id: str = Field(..., alias="_id")
    revision: str = Field(..., alias="_rev")
    document: Dict[str, Any]


class QueryRequest(BaseModel):
    """
    A model for standardizing query request payloads.
    """

    db_name: str
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None


class QueryResponse(BaseModel):
    """
    A model for standardizing query response payloads.
    """

    documents: List[Dict[str, Any]]


def normalize_document_response(raw_response: Dict[str, Any]) -> DocumentResponse:
    """
    Normalizes a raw IBM Cloudant document response into a standardized format.
    """
    return DocumentResponse(
        id=raw_response.get("_id"),
        revision=raw_response.get("_rev"),
        document={k: v for k, v in raw_response.items() if k not in ["_id", "_rev"]},
    )
