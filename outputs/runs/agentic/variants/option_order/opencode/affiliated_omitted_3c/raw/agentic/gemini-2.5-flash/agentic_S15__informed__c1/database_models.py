from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str = Field(..., alias="PK")
    sort_key: str = Field(..., alias="SK")
    content: Dict[str, Any]
    version: int = 1


class DocumentKey(BaseModel):
    id: str = Field(..., alias="PK")
    sort_key: str = Field(..., alias="SK")


class DocumentQuery(BaseModel):
    partition_key: str
    field_name: Optional[str] = None
    field_value: Optional[str] = None
