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
    texts: List[str]
    model: str


@dataclass(frozen=True)
class EmbeddingResponse:
    model: str
    embedding: List[float]


@dataclass(frozen=True)
class BatchEmbeddingResponse:
    model: str
    embeddings: List[List[float]]


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_texts(texts: Sequence[str]) -> List[str]:
    return [normalize_text(t) for t in texts]


def cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same length")
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = sqrt(sum(a * a for a in vec_a))
    mag_b = sqrt(sum(b * b for b in vec_b))
    if not mag_a or not mag_b:
        return 0.0
    return dot / (mag_a * mag_b)


def coerce_embedding(values: Iterable[float]) -> List[float]:
    return [float(v) for v in values]
