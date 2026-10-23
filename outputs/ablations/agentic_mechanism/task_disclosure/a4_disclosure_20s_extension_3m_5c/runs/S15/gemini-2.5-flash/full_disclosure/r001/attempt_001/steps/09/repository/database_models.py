from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class Document(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    value: Any

class DocumentRequest(BaseModel):
    name: str
    value: Any

class DocumentResponse(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    value: Any

def normalize_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Converts MongoDB's _id to id for consistency."""
    if '_id' in doc:
        doc['id'] = str(doc['_id'])
        del doc['_id']
    return doc
