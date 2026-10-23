from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Document(BaseModel):
    document_id: str = Field(..., alias="document_id")
    content: str
    version: int = 1
    attributes: Optional[Dict[str, Any]] = None


class DocumentUpdateRequest(BaseModel):
    content: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
