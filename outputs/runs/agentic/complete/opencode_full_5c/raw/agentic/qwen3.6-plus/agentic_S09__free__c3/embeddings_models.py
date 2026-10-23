from dataclasses import dataclass, field
from typing import List, Optional
import math


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDING_DIMENSIONS = 1536


@dataclass
class EmbeddingRequest:
    model: str = OPENAI_EMBEDDING_MODEL
    input_text: str = ""
    dimensions: Optional[int] = OPENAI_EMBEDDING_DIMENSIONS

    def to_payload(self):
        payload = {"model": self.model, "input": self.input_text}
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        return payload


@dataclass
class BatchEmbeddingRequest:
    model: str = OPENAI_EMBEDDING_MODEL
    input_texts: List[str] = field(default_factory=list)
    dimensions: Optional[int] = OPENAI_EMBEDDING_DIMENSIONS

    def to_payload(self):
        payload = {"model": self.model, "input": self.input_texts}
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        return payload


@dataclass
class EmbeddingResponse:
    embedding: List[float]
    index: int
    object_type: str = "embedding"


@dataclass
class BatchEmbeddingResponse:
    embeddings: List[List[float]]
    model: str
    usage: dict = field(default_factory=dict)

    def __len__(self):
        return len(self.embeddings)


@dataclass
class SimilarityResult:
    text_a: str
    text_b: str
    similarity: float


@dataclass
class SearchResult:
    query: str
    document: str
    score: float
    rank: int


@dataclass
class EmbeddingJobSummary:
    total_texts: int
    successful: int
    failed: int
    avg_tokens: float
    model: str
    total_tokens: int


def normalize_vector(vec):
    magnitude = math.sqrt(sum(x * x for x in vec))
    if magnitude == 0:
        return vec
    return [x / magnitude for x in vec]


def cosine_similarity(vec_a, vec_b):
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimension")
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(x * x for x in vec_a))
    mag_b = math.sqrt(sum(x * x for x in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot_product / (mag_a * mag_b)


def rank_results_by_score(results):
    return sorted(results, key=lambda r: r.score, reverse=True)
