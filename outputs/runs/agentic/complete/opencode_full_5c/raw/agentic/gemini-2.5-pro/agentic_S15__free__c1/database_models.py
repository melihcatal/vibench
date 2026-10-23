from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Document(BaseModel):
    document_id: str
    content: str
    version: int = 1
    author: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    items: list[Document]
    count: int
