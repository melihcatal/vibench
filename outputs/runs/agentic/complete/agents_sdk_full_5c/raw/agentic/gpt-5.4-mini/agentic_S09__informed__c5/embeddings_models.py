from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List, Sequence


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
    embedding: List[float]


@dataclass(frozen=True)
class BatchEmbeddingResponse:
    model: str
    embeddings: List[List[float]]


@dataclass(frozen=True)
class SearchDocument:
    doc_id: str
    text: str
    embedding: List[float]


def normalize_vector(values: Iterable[float]) -> List[float]:
    vec = [float(v) for v in values]
    norm = sqrt(sum(v * v for v in vec))
    if norm == 0:
        return vec
    return [v / norm for v in vec]


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    a_n = normalize_vector(a)
    b_n = normalize_vector(b)
    return float(sum(x * y for x, y in zip(a_n, b_n)))
