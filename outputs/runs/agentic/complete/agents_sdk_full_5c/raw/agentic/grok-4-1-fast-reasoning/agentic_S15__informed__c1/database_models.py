from typing import TypedDict, Any, Dict, List, Optional

class Document(TypedDict):
    doc_id: str
    content: Dict[str, Any]
    version: int

QueryResult = List[Document]