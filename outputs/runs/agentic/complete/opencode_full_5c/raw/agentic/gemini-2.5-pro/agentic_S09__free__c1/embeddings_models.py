from dataclasses import dataclass
from typing import List, Optional


@dataclass
class EmbeddingRequest:
    texts: List[str]
    model: Optional[str] = "embed-english-v3.0"
    input_type: Optional[str] = "search_document"


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]


@dataclass
class SimilarityRequest:
    text1: str
    text2: str


@dataclass
class SimilarityResponse:
    similarity: float


@dataclass
class SearchEmbeddingRequest:
    query: str
    documents: List[str]


@dataclass
class SearchEmbeddingResponse:
    query_embedding: List[float]
    document_embeddings: List[List[float]]
