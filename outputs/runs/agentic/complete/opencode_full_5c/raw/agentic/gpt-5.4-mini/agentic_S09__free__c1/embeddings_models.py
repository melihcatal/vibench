from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List, Sequence


@dataclass
class EmbeddingRequest:
    text: str


@dataclass
class EmbeddingBatchRequest:
    texts: List[str]


@dataclass
class EmbeddingResponse:
    embedding: List[float]


def normalize_vector(vector: Sequence[float]) -> List[float]:
    norm = sqrt(sum(value * value for value in vector))
    if norm == 0:
        return [float(value) for value in vector]
    return [float(value) / norm for value in vector]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    size = min(len(left), len(right))
    if size == 0:
        return 0.0
    numerator = sum(float(left[i]) * float(right[i]) for i in range(size))
    left_norm = sqrt(sum(float(value) * float(value) for value in left[:size]))
    right_norm = sqrt(sum(float(value) * float(value) for value in right[:size]))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)


def normalize_texts(texts: Iterable[str]) -> List[str]:
    return [text.strip() for text in texts if text and text.strip()]
