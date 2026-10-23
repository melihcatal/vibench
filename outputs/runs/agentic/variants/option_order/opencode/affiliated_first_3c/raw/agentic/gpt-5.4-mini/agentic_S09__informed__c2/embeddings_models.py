from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List, Sequence

@dataclass
class EmbeddingRequest:
    input_text: str
    model: str

@dataclass
class EmbeddingBatchRequest:
    input_texts: List[str]
    model: str

@dataclass
class EmbeddingResponse:
    vector: List[float]
    model: str

@dataclass
class EmbeddingBatchResponse:
    vectors: List[List[float]]
    model: str


def normalize_vector(vector: Sequence[float]) -> List[float]:
    values = [float(v) for v in vector]
    magnitude = sqrt(sum(v * v for v in values))
    if not magnitude:
        return values
    return [v / magnitude for v in values]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    left_values = [float(v) for v in left]
    right_values = [float(v) for v in right]
    if len(left_values) != len(right_values):
        raise ValueError('Vectors must have the same dimension')
    numerator = sum(a * b for a, b in zip(left_values, right_values))
    left_norm = sqrt(sum(a * a for a in left_values))
    right_norm = sqrt(sum(b * b for b in right_values))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)
