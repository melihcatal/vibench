from typing import TypedDict, Any

class Document(TypedDict):
    id: str
    _partitionKey: str # Example for partition key, if needed
    # Other fields are dynamic
    
class DocumentPayload(TypedDict):
    id: str
    document: dict[str, Any]
