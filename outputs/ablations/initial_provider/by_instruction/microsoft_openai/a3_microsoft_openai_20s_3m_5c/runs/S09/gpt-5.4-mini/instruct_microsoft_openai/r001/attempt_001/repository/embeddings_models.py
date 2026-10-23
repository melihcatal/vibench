from dataclasses import dataclass
from math import sqrt
from typing import Any, Dict, Iterable, List, Sequence


@dataclass
class EmbeddingRequest:
    input: Any
    model: str


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
    raw: Dict[str, Any]


def normalize_vector(values: Sequence[float]) -> List[float]:
    norm = sqrt(sum(v * v for v in values))
    if not norm:
        return [float(v) for v in values]
    return [float(v) / norm for v in values]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Vectors must have the same length")
    return sum(float(a) * float(b) for a, b in zip(left, right)) / (
        sqrt(sum(float(a) * float(a) for a in left)) * sqrt(sum(float(b) * float(b) for b in right))
        or 1.0
    )


def ensure_text_batch(input_value: Any) -> List[str]:
    if isinstance(input_value, str):
        return [input_value]
    return [str(item) for item in input_value]
