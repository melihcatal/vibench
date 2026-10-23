from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str
    content: Dict[str, Any]
    version: Optional[int] = None


class QueryFilter(BaseModel):
    field_name: str
    field_value: Any


class ConditionalUpdate(BaseModel):
    id: str
    updates: Dict[str, Any]
    expected_version: Optional[int] = None
