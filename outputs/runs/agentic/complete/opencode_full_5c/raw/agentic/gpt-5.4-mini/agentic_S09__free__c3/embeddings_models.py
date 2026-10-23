import math
from dataclasses import dataclass
from typing import Iterable, List, Sequence


@dataclass
class EmbeddingRequest:
    input_texts: Sequence[str]


@dataclass
class EmbeddingResponse:
    vectors: List[List[float]]
    model: str


def normalize_vector(vector: Iterable[float]) -> List[float]:
    values = [float(v) for v in vector]
    norm = math.sqrt(sum(v * v for v in values))
    if not norm:
        return values
    return [v / norm for v in values]


def cosine_similarity(left: Iterable[float], right: Iterable[float]) -> float:
    a = list(left)
    b = list(right)
    limit = min(len(a), len(b))
    if not limit:
        return 0.0
    dot = sum(a[i] * b[i] for i in range(limit))
    na = math.sqrt(sum(a[i] * a[i] for i in range(limit)))
    nb = math.sqrt(sum(b[i] * b[i] for i in range(limit)))
    if not na or not nb:
        return 0.0
    return dot / (na * nb)
