from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class DocumentModel(BaseModel):
    id: str = Field(..., alias="_id")
    data: Dict[str, Any]
    version: int = Field(default=1)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class UpsertRequest(BaseModel):
    document_id: str
    data: Dict[str, Any]


class FetchResponse(BaseModel):
    document: Optional[DocumentModel]


class QueryRequest(BaseModel):
    field: str
    value: Any


class QueryResponse(BaseModel):
    documents: list[DocumentModel]


class ConditionalUpdateRequest(BaseModel):
    document_id: str
    update_data: Dict[str, Any]
    expected_version: int
