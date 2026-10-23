from dataclasses import dataclass
from math import sqrt
from typing import Iterable, Sequence

@dataclass
class EmbeddingRequest:
    input: str | list[str]
    model: str

@dataclass
class EmbeddingResponse:
    vectors: list[list[float]]
    model: str


def normalize_vector(vector: Sequence[float]) -> list[float]:
    norm = sqrt(sum(x * x for x in vector))
    if not norm:
        return [0.0 for _ in vector]
    return [x / norm for x in vector]


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise ValueError('vector dimensions must match')
    return sum(x * y for x, y in zip(a, b)) / (sqrt(sum(x * x for x in a)) * sqrt(sum(y * y for y in b)) or 1.0)


def normalize_texts(texts: Iterable[str]) -> list[str]:
    return [t.strip() for t in texts if t and t.strip()]
