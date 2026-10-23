from dataclasses import dataclass
from math import sqrt
from typing import Any, Iterable, List


@dataclass
class EmbeddingRequest:
    input: Any
    model: str


@dataclass
class EmbeddingResponse:
    vectors: List[List[float]]
    model: str


def normalize_vector(vector: Iterable[float]) -> List[float]:
    values = [float(v) for v in vector]
    norm = sqrt(sum(v * v for v in values)) or 1.0
    return [v / norm for v in values]


def cosine_similarity(left: Iterable[float], right: Iterable[float]) -> float:
    l = list(left)
    r = list(right)
    denom = (sqrt(sum(v * v for v in l)) or 1.0) * (sqrt(sum(v * v for v in r)) or 1.0)
    return sum(a * b for a, b in zip(l, r)) / denom
