from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


class Document(BaseModel):
    id: str = Field(..., description="Primary identifier for the document")
    document: Dict[str, Any] = Field(..., description="The document content")


class QueryCondition(BaseModel):
    field: str
    operator: str
    value: Any


class ConditionalUpdatePayload(BaseModel):
    id: str
    updates: Dict[str, Any]
    condition_field: str
    condition_value: Any
