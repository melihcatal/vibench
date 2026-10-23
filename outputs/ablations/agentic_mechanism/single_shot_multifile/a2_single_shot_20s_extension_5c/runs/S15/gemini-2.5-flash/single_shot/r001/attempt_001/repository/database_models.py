from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class Document(BaseModel):
    id: str = Field(..., description="Unique identifier for the document.")
    title: str
    content: str
    status: Optional[str] = "draft"
    version: int = 1
    metadata: Dict[str, Any] = Field(default_factory=dict)

class UpsertDocumentRequest(BaseModel):
    document: Document

class FetchDocumentResponse(BaseModel):
    document: Optional[Document]

class QueryDocumentsRequest(BaseModel):
    field_name: str
    field_value: Any
    limit: Optional[int] = 10

class QueryDocumentsResponse(BaseModel):
    documents: List[Document] = Field(default_factory=list)

class ConditionalUpdateRequest(BaseModel):
    id: str
    expected_version: int
    updates: Dict[str, Any]
