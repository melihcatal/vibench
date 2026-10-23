from typing import TypedDict, Optional, Dict, Any


class Document(TypedDict):
    document_id: str
    content: str
    version: int
    author: Optional[str]
    metadata: Optional[Dict[str, Any]]


class UpsertResponse(TypedDict):
    success: bool
    document_id: str
    version: int


class FetchResponse(TypedDict):
    success: bool
    document: Optional[Document]


class QueryResponse(TypedDict):
    success: bool
    documents: list[Document]
