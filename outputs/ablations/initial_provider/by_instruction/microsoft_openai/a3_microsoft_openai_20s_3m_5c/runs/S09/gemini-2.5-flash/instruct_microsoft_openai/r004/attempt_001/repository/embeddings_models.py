from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class EmbeddingRequest:
    input: List[str] | str
    model: str

@dataclass
class EmbeddingResponseData:
    embedding: List[float]
    index: int
    object: str

@dataclass
class EmbeddingResponse:
    data: List[EmbeddingResponseData]
    model: str
    object: str
    usage: Dict[str, Any]
