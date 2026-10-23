from typing import TypedDict

class Document(TypedDict):
    """
    A TypedDict representing the structure of a document in the database.
    This helps with static analysis and code completion.
    """
    document_id: str  # Primary partition key
    user_id: str      # Attribute for querying, potentially a GSI partition key
    content: str
    version: int      # For optimistic locking/conditional updates
    last_updated: str # ISO 8601 timestamp
