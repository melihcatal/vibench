from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List, Sequence


@dataclass
class EmbedRequest:
    text: str


@dataclass
class BatchEmbedRequest:
    texts: List[str]


@dataclass
class EmbedResponse:
    vector: List[float]


def normalize_vector(vector: Sequence[float]) -> List[float]:
    norm = sqrt(sum(value * value for value in vector))
    if norm == 0:
        return [float(value) for value in vector]
    return [float(value) / norm for value in vector]


def normalize_vectors(vectors: Iterable[Sequence[float]]) -> List[List[float]]:
    return [normalize_vector(vector) for vector in vectors]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    left_norm = normalize_vector(left)
    right_norm = normalize_vector(right)
    return sum(a * b for a, b in zip(left_norm, right_norm))
