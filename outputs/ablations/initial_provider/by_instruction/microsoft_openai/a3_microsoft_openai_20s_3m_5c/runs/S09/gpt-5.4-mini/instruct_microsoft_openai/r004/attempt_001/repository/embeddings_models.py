from dataclasses import dataclass
from math import sqrt
from typing import List, Sequence


@dataclass
class EmbeddingVector:
    text: str
    vector: List[float]


def vector_from_response_item(item) -> List[float]:
    return list(item.embedding)


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    limit = min(len(a), len(b))
    dot = sum(a[i] * b[i] for i in range(limit))
    na = sqrt(sum(x * x for x in a))
    nb = sqrt(sum(x * x for x in b))
    if not na or not nb:
        return 0.0
    return dot / (na * nb)
