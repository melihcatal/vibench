from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class EmbeddingRequest:
    text: str


@dataclass(frozen=True)
class EmbeddingBatchRequest:
    texts: Sequence[str]


@dataclass(frozen=True)
class EmbeddingResponse:
    vector: List[float]
    model: str


@dataclass(frozen=True)
class BatchEmbeddingResponse:
    vectors: List[List[float]]
    model: str


def normalize_vector(vector: Iterable[float]) -> List[float]:
    values = [float(v) for v in vector]
    norm = sqrt(sum(v * v for v in values))
    if norm == 0:
        return values
    return [v / norm for v in values]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    left_values = [float(v) for v in left]
    right_values = [float(v) for v in right]
    size = min(len(left_values), len(right_values))
    if size == 0:
        return 0.0
    dot = sum(left_values[i] * right_values[i] for i in range(size))
    left_norm = sqrt(sum(v * v for v in left_values[:size]))
    right_norm = sqrt(sum(v * v for v in right_values[:size]))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)
