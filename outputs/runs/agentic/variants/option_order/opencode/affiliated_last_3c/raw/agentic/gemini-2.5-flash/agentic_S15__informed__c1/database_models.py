from pydantic import BaseModel
from typing import Optional, Dict, Any


class Document(BaseModel):
    id: str
    data: Dict[str, Any]


class DocumentUpdate(BaseModel):
    id: str
    updates: Dict[str, Any]
    if_match: Optional[str] = None  # For conditional updates (e.g., ETag or version)
