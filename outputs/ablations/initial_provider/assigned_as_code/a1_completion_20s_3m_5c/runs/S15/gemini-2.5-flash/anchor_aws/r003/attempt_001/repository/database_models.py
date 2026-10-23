from typing import Dict, Any
from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str = Field(..., description="Primary identifier for the document")
    content: Dict[str, Any] = Field(..., description="The document content as a dictionary")


class QueryCondition(BaseModel):
    field_name: str = Field(..., description="The name of the field to query on")
    field_value: Any = Field(..., description="The value to match for the field")
