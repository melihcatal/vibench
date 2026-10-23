from dataclasses import dataclass
from math import sqrt


@dataclass
class EmbeddingRequest:
    inputs: list[str]


@dataclass
class EmbeddingResponse:
    vectors: list[list[float]]


def normalize_vector(vector: list[float]) -> list[float]:
    norm = sqrt(sum(value * value for value in vector))
    if not norm:
        return vector
    return [value / norm for value in vector]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    left_n = normalize_vector(left)
    right_n = normalize_vector(right)
    return sum(a * b for a, b in zip(left_n, right_n))
