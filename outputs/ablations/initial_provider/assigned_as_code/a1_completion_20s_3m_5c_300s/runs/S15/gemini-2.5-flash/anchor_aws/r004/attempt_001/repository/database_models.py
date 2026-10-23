from typing import Dict, Any, Optional
from pydantic import BaseModel

class DocumentPayload(BaseModel):
    id: str
    document: Dict[str, Any]

class DocumentConfig(BaseModel):
    region: str
    table_name: str
    key_field: Optional[str] = "id"

class DocumentRecord(BaseModel):
    id: str
    data: Dict[str, Any]
