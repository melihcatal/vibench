import math
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class EmbeddingRequest:
    text: str
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None
    encoding_format: str = "float"


@dataclass
class BatchEmbeddingRequest:
    texts: List[str]
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None
    encoding_format: str = "float"


@dataclass
class EmbeddingResponse:
    embedding: List[float]
    model: str
    index: int = 0
    usage: Optional[dict] = None


@dataclass
class BatchEmbeddingResponse:
    embeddings: List[List[float]]
    model: str
    count: int = 0
    usage: Optional[dict] = None


@dataclass
class SimilarityResult:
    score: float
    text_a: str
    text_b: str
    vector_a: List[float]
    vector_b: List[float]


@dataclass
class SearchResult:
    query: str
    query_embedding: List[float]
    documents: List[dict]
    ranked_results: List[dict] = field(default_factory=list)


def l2_normalize(vec: List[float]) -> List[float]:
    magnitude = math.sqrt(sum(x * x for x in vec))
    if magnitude == 0:
        return vec
    return [x / magnitude for x in vec]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(x * x for x in vec_a))
    mag_b = math.sqrt(sum(x * x for x in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def to_embedding_request(text, model=None, dimensions=None):
    return EmbeddingRequest(
        text=text,
        model=model or "text-embedding-3-small",
        dimensions=dimensions,
    )


def to_batch_request(texts, model=None, dimensions=None):
    return BatchEmbeddingRequest(
        texts=texts,
        model=model or "text-embedding-3-small",
        dimensions=dimensions,
    )
