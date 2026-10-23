from typing import TypedDict, Optional

class DocumentModel(TypedDict):
    _id: str
    _v: Optional[int]  # version field for conditional updates
    # Add additional fields as needed
    title: Optional[str]
    content: Optional[str]
    created_at: Optional[str]

class QueryFilter(TypedDict):
    # Generic filter keys; values can be exact matches, $regex, etc.
    pass

Model = dict[str, any]  # legacy alias
