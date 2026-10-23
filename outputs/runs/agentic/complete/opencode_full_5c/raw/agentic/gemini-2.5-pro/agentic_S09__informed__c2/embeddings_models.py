from pydantic import BaseModel
from typing import List


class EmbeddingRequest(BaseModel):
    text: str


class BatchEmbeddingRequest(BaseModel):
    texts: List[str]


class EmbeddingResponse(BaseModel):
    embedding: List[float]


class BatchEmbeddingResponse(BaseModel):
    embeddings: List[List[float]]


class SimilarityRequest(BaseModel):
    text1: str
    text2: str


class SimilarityResponse(BaseModel):
    score: float


class SearchRequest(BaseModel):
    query: str
    documents: List[str]


class SearchEmbeddingResponse(BaseModel):
    query_embedding: List[float]
    document_embeddings: List[List[float]]
