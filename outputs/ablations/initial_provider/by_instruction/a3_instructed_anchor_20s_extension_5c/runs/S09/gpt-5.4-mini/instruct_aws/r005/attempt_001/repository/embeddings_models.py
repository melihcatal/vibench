from dataclasses import dataclass
from math import sqrt
from typing import Iterable, Sequence


@dataclass
class EmbeddingRequest:
    text: str


@dataclass
class BatchEmbeddingRequest:
    texts: list[str]


@dataclass
class EmbeddingResponse:
    model_id: str
    embedding: list[float]


def normalize_embedding(values: Sequence[float]) -> list[float]:
    vector = [float(v) for v in values]
    magnitude = sqrt(sum(v * v for v in vector))
    if not magnitude:
        return vector
    return [v / magnitude for v in vector]


def cosine_similarity(left: Iterable[float], right: Iterable[float]) -> float:
    left_vec = [float(v) for v in left]
    right_vec = [float(v) for v in right]
    if len(left_vec) != len(right_vec):
        raise ValueError("Vectors must have the same length")
    dot = sum(a * b for a, b in zip(left_vec, right_vec))
    left_mag = sqrt(sum(a * a for a in left_vec))
    right_mag = sqrt(sum(b * b for b in right_vec))
    if not left_mag or not right_mag:
        return 0.0
    return dot / (left_mag * right_mag)
