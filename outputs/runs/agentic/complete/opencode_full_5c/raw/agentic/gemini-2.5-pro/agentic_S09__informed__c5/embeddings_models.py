from typing import List, Dict, Any
from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    texts: List[str]


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]


class SimilarityRequest(BaseModel):
    text1: str
    text2: str


class SimilarityResponse(BaseModel):
    similarity: float


class SearchEmbeddingRequest(BaseModel):
    query: str
    documents: List[str]


class SearchEmbeddingResponse(BaseModel):
    query_embedding: List[float]
    document_embeddings: List[List[float]]


def normalize_vector(vector: List[float]) -> List[float]:
    magnitude = sum(v**2 for v in vector) ** 0.5
    if magnitude == 0:
        return vector
    return [v / magnitude for v in vector]
