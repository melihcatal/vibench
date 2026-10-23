from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class EmbeddingRequest:
    text: str
    model: str = "text-embedding-ada-002"

@dataclass
class BatchEmbeddingRequest:
    texts: List[str]
    model: str = "text-embedding-ada-002"

@dataclass
class EmbeddingResponse:
    embedding: List[float]
    model: str
    usage: Dict[str, Any]

@dataclass
class BatchEmbeddingResponse:
    embeddings: List[List[float]]
    model: str
    usage: Dict[str, Any]

def normalize_text(text: str) -> str:
    return text.strip().replace("\n", " ")
