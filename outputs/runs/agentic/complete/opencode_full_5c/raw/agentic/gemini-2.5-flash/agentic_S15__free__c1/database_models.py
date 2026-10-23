from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Document(BaseModel):
    id: str = Field(..., alias="_id")
    content: Dict[str, Any]
    version: Optional[int] = 1


class UpsertDocumentRequest(BaseModel):
    document: Document


class FetchDocumentRequest(BaseModel):
    document_id: str


class QueryDocumentsRequest(BaseModel):
    field_name: str
    field_value: Any


class ConditionalUpdateRequest(BaseModel):
    document_id: str
    updates: Dict[str, Any]
    expected_version: int


class DocumentResponse(BaseModel):
    document: Optional[Document]
    message: str
