from typing import TypedDict, Dict, Any

# Simple normalized document representation for internal use

class Document(TypedDict):
    id: str
    data: Dict[str, Any]
