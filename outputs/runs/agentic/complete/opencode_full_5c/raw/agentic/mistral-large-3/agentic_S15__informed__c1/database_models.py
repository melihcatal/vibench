from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class DocumentRequest(BaseModel):
    document_id: str
    document_data: Dict[str, Any]


class DocumentResponse(BaseModel):
    document_id: str
    document_data: Dict[str, Any]


class QueryRequest(BaseModel):
    field: str
    value: Any


class QueryResponse(BaseModel):
    documents: List[Dict[str, Any]]


class ConditionalUpdateRequest(BaseModel):
    document_id: str
    condition_field: str
    condition_value: Any
    update_data: Dict[str, Any]
