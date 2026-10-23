from pydantic import BaseModel, Field
from typing import List, Optional


class EmbeddingRequest(BaseModel):
    texts: List[str]
    task_type: str = "RETRIEVAL_DOCUMENT"
    output_dimensionality: Optional[int] = None


class EmbeddingPrediction(BaseModel):
    embeddings: List[List[float]]


class EmbeddingResponse(BaseModel):
    predictions: List[EmbeddingPrediction]


class SimilarityRequest(BaseModel):
    text_a: str
    text_b: str


class SimilarityResponse(BaseModel):
    similarity: float


class SearchEmbeddingRequest(BaseModel):
    query: str
    documents: List[str]


class SearchEmbeddingResponse(BaseModel):
    query_embedding: List[float]
    document_embeddings: List[List[float]]


def normalize_vector(vector: List[float]) -> List[float]:
    norm = sum(v * v for v in vector) ** 0.5
    if norm == 0:
        return vector
    return [v / norm for v in vector]
