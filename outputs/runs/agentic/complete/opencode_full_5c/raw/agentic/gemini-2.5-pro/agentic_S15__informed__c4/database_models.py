from pydantic import BaseModel, Field
from typing import Optional


class Document(BaseModel):
    doc_id: str = Field(..., alias="doc_id")
    content: str
    author: str
    version: int = 1
