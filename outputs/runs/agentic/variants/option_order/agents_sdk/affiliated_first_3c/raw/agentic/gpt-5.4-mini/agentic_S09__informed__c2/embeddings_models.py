from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence


@dataclass(frozen=True)
class EmbeddingRequest:
    text: str
    model: str


@dataclass(frozen=True)
class BatchEmbeddingRequest:
    texts: Sequence[str]
    model: str


@dataclass(frozen=True)
class EmbeddingResponse:
    model: str
    embedding: list[float]
    usage: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BatchEmbeddingResponse:
    model: str
    embeddings: list[list[float]]
    usage: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SearchDocument:
    id: str
    text: str
    embedding: list[float]


@dataclass(frozen=True)
class SearchBundle:
    query: str
    query_embedding: list[float]
    documents: list[SearchDocument]


def coerce_embedding(values: Iterable[float]) -> list[float]:
    return [float(v) for v in values]


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise ValueError("embedding dimensions must match")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)
