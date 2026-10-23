from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class EmbeddingRequest:
    input_text: str
    model: str


@dataclass(frozen=True)
class BatchEmbeddingRequest:
    texts: Sequence[str]
    model: str


@dataclass(frozen=True)
class EmbeddingResponse:
    vector: List[float]
    model: str


def normalize_vector(vector: Iterable[float]) -> List[float]:
    values = [float(v) for v in vector]
    norm = sqrt(sum(v * v for v in values))
    if norm == 0:
        return values
    return [v / norm for v in values]


def cosine_similarity(vector_a: Sequence[float], vector_b: Sequence[float]) -> float:
    a = list(vector_a)
    b = list(vector_b)
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sqrt(sum(x * x for x in a))
    norm_b = sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
