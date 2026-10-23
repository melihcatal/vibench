from dataclasses import dataclass
from math import sqrt
from typing import Iterable, Sequence


@dataclass(frozen=True)
class EmbeddingRequest:
    texts: list[str]


@dataclass(frozen=True)
class EmbeddingResponse:
    model: str
    vectors: list[list[float]]


def normalize_vector(vector: Sequence[float]) -> list[float]:
    norm = sqrt(sum(value * value for value in vector))
    if norm == 0:
        return [float(value) for value in vector]
    return [float(value) / norm for value in vector]


def normalize_vectors(vectors: Iterable[Sequence[float]]) -> list[list[float]]:
    return [normalize_vector(vector) for vector in vectors]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    left_n = normalize_vector(left)
    right_n = normalize_vector(right)
    return float(sum(a * b for a, b in zip(left_n, right_n)))
