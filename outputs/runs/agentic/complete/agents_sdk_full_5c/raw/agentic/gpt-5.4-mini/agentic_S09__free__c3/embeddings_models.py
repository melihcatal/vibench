"""Request and response models for OpenAI embeddings workflows."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class EmbeddingRequest:
    inputs: Sequence[str]
    model: str


@dataclass(frozen=True)
class EmbeddingResponse:
    vectors: List[List[float]]
    model: str


@dataclass(frozen=True)
class SearchDocument:
    doc_id: str
    text: str


@dataclass(frozen=True)
class SearchResult:
    doc_id: str
    score: float
    text: str


def normalize_texts(texts: Iterable[str]) -> List[str]:
    return [" ".join(str(t).split()) for t in texts if str(t).strip()]


def normalize_vector(vector: Iterable[float]) -> List[float]:
    return [float(x) for x in vector]


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)
