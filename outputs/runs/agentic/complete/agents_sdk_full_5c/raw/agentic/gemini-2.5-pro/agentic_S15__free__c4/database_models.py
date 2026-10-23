from typing import Dict, Any
from pydantic import BaseModel, Field

class Document(BaseModel):
    """
    Represents a document to be stored in the NoSQL database.
    """
    document_id: str = Field(..., description="The primary identifier for the document.")
    category: str = Field(..., description="The category or partition for the document.")
    content: str = Field(..., description="The main content of the document.")
    version: int = Field(default=1, description="The version number for optimistic locking.")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="A flexible dict for other metadata.")
