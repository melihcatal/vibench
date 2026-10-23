from typing import TypedDict, Optional


class Document(TypedDict):
    document_id: str
    content: str
    author: str
    version: int
    created_at: str


class DocumentUpdate(TypedDict):
    content: Optional[str]
    author: Optional[str]
