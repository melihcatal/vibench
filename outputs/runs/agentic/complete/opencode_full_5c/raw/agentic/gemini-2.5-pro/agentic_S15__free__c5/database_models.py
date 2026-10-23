from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Document(BaseModel):
    document_id: str = Field(..., alias="documentId")
    version: int
    content: Dict[str, Any]
    user_id: str = Field(..., alias="userId")


class DocumentUpdate(BaseModel):
    content: Optional[Dict[str, Any]] = None
    version: int
