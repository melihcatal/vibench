from pydantic import BaseModel
from typing import Dict, Any, Optional, List


class UpsertRequest(BaseModel):
    document_id: str
    document: Dict[str, Any]


class UpsertResponse(BaseModel):
    success: bool
    document_id: str
    version: Optional[str] = None
    error: Optional[str] = None


class FetchRequest(BaseModel):
    document_id: str


class FetchResponse(BaseModel):
    success: bool
    document: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class QueryRequest(BaseModel):
    field_name: str
    field_value: Any


class QueryResponse(BaseModel):
    success: bool
    documents: List[Dict[str, Any]] = []
    error: Optional[str] = None


class ConditionalUpdateRequest(BaseModel):
    document_id: str
    updates: Dict[str, Any]
    current_version: Optional[str] = None
    new_version: Optional[str] = None


class ConditionalUpdateResponse(BaseModel):
    success: bool
    document: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
