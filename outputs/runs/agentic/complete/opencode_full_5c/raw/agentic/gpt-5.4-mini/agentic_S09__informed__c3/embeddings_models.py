from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class EmbeddingRequest:
    input_text: str


@dataclass(frozen=True)
class EmbeddingBatchRequest:
    input_texts: List[str]


@dataclass(frozen=True)
class EmbeddingResponse:
    vector: List[float]
    model: str


def normalize_vector(vector: Sequence[float]) -> List[float]:
    values = [float(v) for v in vector]
    norm = sqrt(sum(v * v for v in values))
    if norm == 0.0:
        return values
    return [v / norm for v in values]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    left_values = list(left)
    right_values = list(right)
    length = min(len(left_values), len(right_values))
    if length == 0:
        return 0.0
    left_values = left_values[:length]
    right_values = right_values[:length]
    left_norm = normalize_vector(left_values)
    right_norm = normalize_vector(right_values)
    return sum(a * b for a, b in zip(left_norm, right_norm))


def ensure_texts(texts: Iterable[str]) -> List[str]:
    return [str(text) for text in texts]
