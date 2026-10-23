from typing import TypedDict, Optional, Dict, Any

class Document(TypedDict):
    """
    Represents the structure of a document in the database.
    """
    id: str
    category: str
    version: int
    content: Dict[str, Any]

class ConditionalUpdateRequest(TypedDict):
    """
    Defines the payload for a conditional update request.
    """
    id: str
    expected_version: int
    new_content: Dict[str, Any]
