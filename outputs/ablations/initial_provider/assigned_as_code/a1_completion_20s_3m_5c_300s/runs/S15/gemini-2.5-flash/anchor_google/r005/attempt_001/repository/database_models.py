from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Document(BaseModel):
    id: str = Field(..., description="Unique identifier for the document")
    data: Dict[str, Any] = Field(..., description="The document content")
    version: Optional[int] = Field(None, description="Version of the document for optimistic locking")


class DocumentQuery(BaseModel):
    field: str = Field(..., description="Field to query by")
    value: Any = Field(..., description="Value to match")
    collection: str = Field(..., description="Firestore collection name")


class ConditionalUpdate(BaseModel):
    id: str = Field(..., description="Unique identifier for the document")
    updates: Dict[str, Any] = Field(..., description="Fields to update")
    collection: str = Field(..., description="Firestore collection name")
    current_version: int = Field(..., description="Current version of the document for conditional update")
    new_version: int = Field(..., description="New version of the document after update")
