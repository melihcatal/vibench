from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class EmbeddingRequest:
    texts: List[str]
    model: str = 'text-embedding-3-small'

@dataclass
class EmbeddingResponse:
    embedding: List[float]

@dataclass
class BatchEmbeddingResponse:
    embeddings: List[List[float]]

@dataclass
class SimilarityScoreResponse:
    score: float
