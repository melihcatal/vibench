from typing import Any, Dict, List, Optional, TypedDict


class Document(TypedDict):
    doc_id: str
    data: Dict[str, Any]
    version: int
    created_at: str
    updated_at: str
