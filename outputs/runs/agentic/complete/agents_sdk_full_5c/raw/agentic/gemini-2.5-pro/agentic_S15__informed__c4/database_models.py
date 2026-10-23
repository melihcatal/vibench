from pydantic import BaseModel, Field
from typing import Dict, Any

class Document(BaseModel):
    """
    A Pydantic model representing a document to be stored in the database.
    This provides basic type validation and serialization for API interactions.
    """
    id: str
    category: str
    content: str
    version: int = Field(default=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)
