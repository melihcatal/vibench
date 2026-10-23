from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class Document(BaseModel):
    id: str = Field(..., description="Primary identifier for the document.")
    content: Dict[str, Any] = Field(..., description="The main content of the document.")
    version: Optional[int] = Field(None, description="Version of the document for optimistic locking.")
    created_at: Optional[str] = Field(None, description="Timestamp when the document was created.")
    updated_at: Optional[str] = Field(None, description="Timestamp when the document was last updated.")

class QueryCondition(BaseModel):
    field_name: str = Field(..., description="The name of the field to query by.")
    field_value: Any = Field(..., description="The value to match for the query.")
    operator: str = Field("=", description="Comparison operator (e.g., =, <, >, <=, >=, begins_with).")
