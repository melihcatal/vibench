from typing import TypedDict, Optional


class Document(TypedDict):
    category: str
    id: str
    content: str
    version: int


class DocumentUpdate(TypedDict):
    content: Optional[str]
