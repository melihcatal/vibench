from pydantic import BaseModel, Field
from typing import Optional

TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME', 'my-documents-table')

class Document(BaseModel):
    id: str
    title: str
    content: str
    author: Optional[str] = None
    status: Optional[str] = 'draft'
    version: int = 1
    created_at: Optional[str] = None # ISO 8601 string
    updated_at: Optional[str] = None # ISO 8601 string

