from typing import TypedDict, List, Optional, Dict, Any

class CryptoEvent(TypedDict):
    timestamp: str
    operation: str
    key_id: str
    principal_id: Optional[str]
    error_code: Optional[str]
    bytes_processed: Optional[int]

class SafetyResult(TypedDict):
    hate: Optional[Dict[str, Any]]
    sexual: Optional[Dict[str, Any]]
    violence: Optional[Dict[str, Any]]

class EmbeddingResponse(TypedDict):
    embedding: List[float]
    model: str