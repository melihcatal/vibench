from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Document(BaseModel):
    id: str = Field(..., description="Primary identifier for the document")
    version: int = Field(1, description="Document version for optimistic locking")
    content: Dict[str, Any] = Field(..., description="The main content of the document")
    partition_key: str = Field(..., description="Partition key for DynamoDB queries")
