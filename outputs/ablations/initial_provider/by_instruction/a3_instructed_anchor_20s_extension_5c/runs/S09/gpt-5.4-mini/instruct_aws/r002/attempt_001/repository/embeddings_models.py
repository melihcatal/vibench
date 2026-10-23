from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class EmbedRequest:
    text: str


@dataclass(frozen=True)
class EmbedBatchRequest:
    texts: list[str]


@dataclass(frozen=True)
class EmbedResponse:
    embedding: list[float]


def normalize_vector(vector: list[float]) -> list[float]:
    norm = sqrt(sum(value * value for value in vector))
    return [value / norm for value in vector] if norm else vector


def cosine_similarity(left: list[float], right: list[float]) -> float:
    left_n = normalize_vector(left)
    right_n = normalize_vector(right)
    return sum(a * b for a, b in zip(left_n, right_n))
