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
    vector: List[float]
    model: str


@dataclass(frozen=True)
class BatchEmbeddingResponse:
    vectors: List[List[float]]
    model: str


@dataclass(frozen=True)
class SearchDocument:
    id: str
    text: str
    score: float | None = None
    embedding: List[float] | None = None


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_texts(texts: Iterable[str]) -> List[str]:
    return [normalize_text(t) for t in texts]


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = sqrt(sum(x * x for x in a))
    mag_b = sqrt(sum(y * y for y in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)
