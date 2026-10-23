from pydantic import BaseModel
from typing import Optional, Dict, Any

class Document(BaseModel):
    id: str
    data: Dict[str, Any]
    version: Optional[str] = None
