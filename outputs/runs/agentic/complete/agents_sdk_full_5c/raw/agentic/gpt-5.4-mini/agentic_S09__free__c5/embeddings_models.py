from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class EmbeddingRequest:
    input_texts: Sequence[str]
    model: str


@dataclass(frozen=True)
class EmbeddingResponse:
    model: str
    vectors: List[List[float]]


@dataclass(frozen=True)
class SimilarityResult:
    score: float


def normalize_vector(vector: Sequence[float]) -> List[float]:
    norm = sqrt(sum(x * x for x in vector))
    if norm == 0:
        return [0.0 for _ in vector]
    return [x / norm for x in vector]


def normalize_vectors(vectors: Iterable[Sequence[float]]) -> List[List[float]]:
    return [normalize_vector(v) for v in vectors]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    left_n = normalize_vector(left)
    right_n = normalize_vector(right)
    return sum(a * b for a, b in zip(left_n, right_n))
