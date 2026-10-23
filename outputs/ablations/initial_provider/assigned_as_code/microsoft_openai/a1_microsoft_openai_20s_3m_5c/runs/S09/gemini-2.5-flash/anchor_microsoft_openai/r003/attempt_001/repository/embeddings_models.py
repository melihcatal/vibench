import dataclasses
from typing import List, Dict, Any

@dataclasses.dataclass
class EmbeddingRequest:
    texts: List[str]
    model: str = "text-embedding-3-small"

@dataclasses.dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]

@dataclasses.dataclass
class SearchRequest:
    query: str
    documents: List[str]
    model: str = "text-embedding-3-small"

@dataclasses.dataclass
class SearchResponse:
    query_embedding: List[float]
    document_embeddings: List[List[float]]
