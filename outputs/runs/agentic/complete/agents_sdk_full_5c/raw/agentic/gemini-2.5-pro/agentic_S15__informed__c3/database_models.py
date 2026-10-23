from typing import Dict, Any
from pydantic import BaseModel, Field

class Document(BaseModel):
    """
    Represents a document to be stored in the database.
    Pydantic model for data validation and serialization.
    """
    id: str = Field(..., description="The unique identifier for the document.")
    author: str = Field(..., description="The author of the document.")
    content: str = Field(..., description="The main content of the document.")
    version: int = Field(1, description="The version number for optimistic locking.")

    def to_dynamodb_item(self) -> Dict[str, Any]:
        """Converts the Pydantic model to a DynamoDB item dictionary."""
        return self.model_dump()

    @classmethod
    def from_dynamodb_item(cls, item: Dict[str, Any]) -> "Document":
        """Creates a Document instance from a DynamoDB item dictionary."""
        return cls(**item)
