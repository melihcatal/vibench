from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

class Document(BaseModel):
    id: str = Field(..., description="Unique identifier of the document")
    data: Dict[str, Any] = Field(..., description="The content of the document")
    version: int = Field(0, description="Version of the document, used for optimistic locking")

class CreateDocumentRequest(BaseModel):
    document: Dict[str, Any] = Field(..., description="The document content to create")

class UpdateDocumentRequest(BaseModel):
    id: str = Field(..., description="Unique identifier of the document to update")
    updates: Dict[str, Any] = Field(..., description="Fields to update in the document")
    expected_version: Optional[int] = Field(None, description="Expected version for conditional update")

class DocumentResponse(BaseModel):
    document: Optional[Document] = None
    message: str

def normalize_document(doc_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a document's data by applying common transformations.
    This is a placeholder for actual normalization logic.
    """
    # Example: Ensure 'created_at' and 'updated_at' fields exist
    normalized_data = doc_data.copy()
    if "created_at" not in normalized_data:
        normalized_data["created_at"] = "CURRENT_TIMESTAMP" # Placeholder for actual timestamp
    normalized_data["updated_at"] = "CURRENT_TIMESTAMP" # Placeholder for actual timestamp
    return normalized_data
