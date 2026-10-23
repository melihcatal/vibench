from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class EmbeddingRequest:
    input_text: str
    model: str


@dataclass(frozen=True)
class EmbeddingBatchRequest:
    texts: Sequence[str]
    model: str


@dataclass(frozen=True)
class EmbeddingResponse:
    vector: List[float]
    model: str


@dataclass(frozen=True)
class EmbeddingBatchResponse:
    vectors: List[List[float]]
    model: str


@dataclass(frozen=True)
class SearchDocument:
    id: str
    text: str


@dataclass(frozen=True)
class SearchResult:
    id: str
    score: float
    text: str


def normalize_vector(vector: Iterable[float]) -> List[float]:
    values = [float(v) for v in vector]
    norm = sqrt(sum(v * v for v in values))
    if norm == 0:
        return values
    return [v / norm for v in values]


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    dot = sum(float(x) * float(y) for x, y in zip(a, b))
    na = sqrt(sum(float(x) * float(x) for x in a))
    nb = sqrt(sum(float(y) * float(y) for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)
