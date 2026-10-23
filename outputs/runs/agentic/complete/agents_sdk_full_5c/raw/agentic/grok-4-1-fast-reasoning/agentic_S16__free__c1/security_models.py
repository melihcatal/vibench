from typing import TypedDict, Dict, Any, Optional, List

class SecretRequest(TypedDict):
    name: str
    version: Optional[str]

class SecretResponse(TypedDict):
    value: str
    version: str
    metadata: Dict[str, Any]

class SafetyResult(TypedDict):
    score: float
    unsafe: bool

class EmbeddingResult(TypedDict):
    embedding: List[float]