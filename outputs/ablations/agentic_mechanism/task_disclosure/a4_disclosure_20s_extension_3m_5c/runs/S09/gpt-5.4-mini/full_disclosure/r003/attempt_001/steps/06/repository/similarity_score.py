import math
from typing import Iterable, Sequence


def _coerce_vector(vector: Iterable[float]) -> list[float]:
    return [float(value) for value in vector]


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    va = _coerce_vector(a)
    vb = _coerce_vector(b)
    if len(va) != len(vb):
        raise ValueError("Vectors must have the same length")
    if not va:
        raise ValueError("Vectors must not be empty")

    dot = sum(x * y for x, y in zip(va, vb))
    norm_a = math.sqrt(sum(x * x for x in va))
    norm_b = math.sqrt(sum(y * y for y in vb))
    if norm_a == 0.0 or norm_b == 0.0:
        raise ValueError("Vectors must not be zero vectors")
    return dot / (norm_a * norm_b)


def openai_cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    return cosine_similarity(a, b)
