from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List


@dataclass
class EmbeddingRequest:
    text: str


@dataclass
class EmbeddingBatchRequest:
    texts: List[str]


@dataclass
class EmbeddingResponse:
    vector: List[float]


def normalize_vector(values: Iterable[float]) -> List[float]:
    vector = [float(v) for v in values]
    norm = sqrt(sum(v * v for v in vector))
    if norm == 0.0:
        return vector
    return [v / norm for v in vector]


def cosine_similarity(left: Iterable[float], right: Iterable[float]) -> float:
    l = list(left)
    r = list(right)
    if len(l) != len(r):
        raise ValueError("Embedding vectors must have the same length")
    return sum(a * b for a, b in zip(l, r)) / (sqrt(sum(a * a for a in l)) * sqrt(sum(b * b for b in r)) or 1.0)
