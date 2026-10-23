from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List, Sequence


@dataclass
class EmbeddingRequest:
    input_texts: Sequence[str]
    model: str


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
    model: str


def normalize_vector(vector: Iterable[float]) -> List[float]:
    values = [float(v) for v in vector]
    norm = sqrt(sum(v * v for v in values))
    return [v / norm for v in values] if norm else values


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    size = min(len(left), len(right))
    if not size:
        return 0.0
    dot = sum(float(left[i]) * float(right[i]) for i in range(size))
    left_norm = sqrt(sum(float(x) * float(x) for x in left[:size]))
    right_norm = sqrt(sum(float(x) * float(x) for x in right[:size]))
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0
