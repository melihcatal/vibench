from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List, Sequence


@dataclass
class EmbeddingRequest:
    text: str


@dataclass
class EmbeddingBatchRequest:
    texts: Sequence[str]


@dataclass
class EmbeddingResponse:
    embedding: List[float]


def normalize_embedding(values: Iterable[float]) -> List[float]:
    vector = [float(v) for v in values]
    norm = sqrt(sum(v * v for v in vector))
    if norm == 0.0:
        return vector
    return [v / norm for v in vector]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    denom_left = sqrt(sum(v * v for v in left))
    denom_right = sqrt(sum(v * v for v in right))
    if denom_left == 0.0 or denom_right == 0.0:
        return 0.0
    return sum(a * b for a, b in zip(left, right)) / (denom_left * denom_right)
