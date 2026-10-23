from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_id: str = Field(..., alias="id")
    partition_key: str
    data: Dict[str, Any]

    class Config:
        allow_population_by_field_name = True


class DocumentResponse(BaseModel):
    document_id: str = Field(..., alias="id")
    partition_key: str
    data: Dict[str, Any]
    etag: Optional[str] = None

    class Config:
        allow_population_by_field_name = True


class QueryRequest(BaseModel):
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None


class QueryResponse(BaseModel):
    documents: List[DocumentResponse]


def normalize_document(document: Dict[str, Any]) -> DocumentResponse:
    return DocumentResponse(**document)
