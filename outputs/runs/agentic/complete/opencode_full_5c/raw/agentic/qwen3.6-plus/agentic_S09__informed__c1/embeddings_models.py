from dataclasses import dataclass, field
from typing import List, Optional
import math


@dataclass
class EmbeddingRequest:
    model: str = "text-embedding-3-small"
    input_text: str = ""
    encoding_format: str = "float"
    dimensions: Optional[int] = None

    def to_payload(self) -> dict:
        payload = {
            "model": self.model,
            "input": self.input_text,
            "encoding_format": self.encoding_format,
        }
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        return payload


@dataclass
class BatchEmbeddingRequest:
    model: str = "text-embedding-3-small"
    input_texts: List[str] = field(default_factory=list)
    encoding_format: str = "float"
    dimensions: Optional[int] = None

    def to_payload(self) -> dict:
        payload = {
            "model": self.model,
            "input": self.input_texts,
            "encoding_format": self.encoding_format,
        }
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        return payload


@dataclass
class EmbeddingResponse:
    embedding: List[float]
    model: str = ""
    usage_tokens: int = 0

    @property
    def dimension(self) -> int:
        return len(self.embedding)


@dataclass
class BatchEmbeddingResponse:
    embeddings: List[List[float]]
    models: List[str] = field(default_factory=list)
    usage_tokens: int = 0

    @property
    def count(self) -> int:
        return len(self.embeddings)

    @property
    def dimension(self) -> int:
        if self.embeddings:
            return len(self.embeddings[0])
        return 0


@dataclass
class SearchResult:
    query_embedding: List[float]
    document_embeddings: List[List[float]]
    documents: List[str]
    scores: List[float] = field(default_factory=list)


def normalize_vector(vector: List[float]) -> List[float]:
    magnitude = math.sqrt(sum(x * x for x in vector))
    if magnitude == 0:
        return vector
    return [x / magnitude for x in vector]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(x * x for x in vec_a))
    norm_b = math.sqrt(sum(x * x for x in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def rank_documents_by_similarity(
    query_embedding: List[float],
    document_embeddings: List[List[float]],
    documents: List[str],
    top_k: Optional[int] = None,
) -> SearchResult:
    scores = [
        cosine_similarity(query_embedding, doc_emb) for doc_emb in document_embeddings
    ]
    indexed = list(enumerate(scores))
    indexed.sort(key=lambda x: x[1], reverse=True)
    if top_k is not None:
        indexed = indexed[:top_k]
    sorted_docs = [documents[i] for i, _ in indexed]
    sorted_embeddings = [document_embeddings[i] for i, _ in indexed]
    sorted_scores = [score for _, score in indexed]
    return SearchResult(
        query_embedding=query_embedding,
        document_embeddings=sorted_embeddings,
        documents=sorted_docs,
        scores=sorted_scores,
    )
