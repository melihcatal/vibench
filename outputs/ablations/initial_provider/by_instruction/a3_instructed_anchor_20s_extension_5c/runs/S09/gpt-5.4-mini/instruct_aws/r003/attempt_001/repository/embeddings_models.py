from dataclasses import dataclass
from math import sqrt
from typing import List, Sequence


@dataclass
class EmbeddingRequest:
    text: str


@dataclass
class BatchEmbeddingRequest:
    texts: List[str]


@dataclass
class EmbeddingResponse:
    embedding: List[float]


def normalize_embedding(values: Sequence[float]) -> List[float]:
    vector = [float(v) for v in values]
    magnitude = sqrt(sum(v * v for v in vector)) or 1.0
    return [v / magnitude for v in vector]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    left_vec = list(left)
    right_vec = list(right)
    length = min(len(left_vec), len(right_vec))
    if length == 0:
        return 0.0
    dot = sum(left_vec[i] * right_vec[i] for i in range(length))
    left_norm = sqrt(sum(v * v for v in left_vec)) or 1.0
    right_norm = sqrt(sum(v * v for v in right_vec)) or 1.0
    return dot / (left_norm * right_norm)
