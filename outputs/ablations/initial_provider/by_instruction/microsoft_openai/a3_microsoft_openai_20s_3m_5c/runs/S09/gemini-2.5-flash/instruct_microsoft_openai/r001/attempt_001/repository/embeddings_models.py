import dataclasses
from typing import List, Dict, Any

@dataclasses.dataclass
class EmbeddingRequest:
    input: List[str]
    model: str = "text-embedding-ada-002"

@dataclasses.dataclass
class EmbeddingResponse:
    object: str
    data: List[Dict[str, Any]]
    model: str
    usage: Dict[str, Any]
