from pydantic import BaseModel, Field
from typing import Optional


class Document(BaseModel):
    id: str = Field(..., alias="document_id")
    title: str
    content: str
    status: Optional[str] = "draft"
    version: int = 1


class DocumentUpsertRequest(BaseModel):
    document: Document


class DocumentFetchRequest(BaseModel):
    document_id: str


class DocumentQueryRequest(BaseModel):
    field: str
    value: str


class DocumentConditionalUpdateRequest(BaseModel):
    document_id: str
    updates: dict
    expected_version: int
