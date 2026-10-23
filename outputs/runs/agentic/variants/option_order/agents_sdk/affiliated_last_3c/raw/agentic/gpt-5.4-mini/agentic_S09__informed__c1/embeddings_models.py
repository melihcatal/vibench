from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Sequence


@dataclass(slots=True)
class EmbeddingRequest:
    texts: list[str]
    model: str
    dimensions: int | None = None

    def normalized_texts(self) -> list[str]:
        return [normalize_text(t) for t in self.texts]


@dataclass(slots=True)
class EmbeddingResponse:
    model: str
    embeddings: list[list[float]]
    provider: str = "openai"
    usage: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SearchDocument:
    id: str
    text: str
    embedding: list[float] | None = None
    score: float | None = None


@dataclass(slots=True)
class SearchResult:
    query_embedding: list[float]
    documents: list[SearchDocument]


@dataclass(slots=True)
class EmbeddingJobSummary:
    job_id: str
    total_records: int
    embedded_records: int
    failed_records: int
    model: str


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_embedding_vector(vector: Sequence[Any]) -> list[float]:
    return [float(x) for x in vector]


def cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    a = normalize_embedding_vector(vec_a)
    b = normalize_embedding_vector(vec_b)
    if len(a) != len(b):
        raise ValueError("Embedding vectors must have the same length")
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = sum(x * x for x in a) ** 0.5
    mag_b = sum(y * y for y in b) ** 0.5
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)
