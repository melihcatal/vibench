from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class EmbeddingRequest:
    input_texts: List[str]


@dataclass
class EmbeddingResponse:
    vectors: List[List[float]]
    model: str


def normalize_vector(vector: Iterable[float]) -> List[float]:
    values = [float(x) for x in vector]
    norm = sum(x * x for x in values) ** 0.5
    return [x / norm for x in values] if norm else values


def cosine_similarity(left: Iterable[float], right: Iterable[float]) -> float:
    a = list(left)
    b = list(right)
    denom = (sum(x * x for x in a) ** 0.5) * (sum(x * x for x in b) ** 0.5)
    return sum(x * y for x, y in zip(a, b)) / denom if denom else 0.0
