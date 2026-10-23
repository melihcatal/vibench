from typing import TypedDict, Optional, List

class Document(TypedDict):
    """
    Represents the structure of a document in the database.
    'id' is the primary key.
    'partitionKey' is used for querying a group of documents.
    'version' is for optimistic locking.
    """
    id: str
    partitionKey: str
    content: str
    version: int
    tags: Optional[List[str]]

class ConditionalUpdateRequest(TypedDict):
    """
    Defines the payload for a conditional update operation.
    """
    document_id: str
    update_expression: str
    expression_attribute_values: dict
    condition_expression: str
