from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class EmbeddingRequest:
    texts: List[str]
    model: str
    dimensions: int | None = None


@dataclass(frozen=True)
class EmbeddingResponse:
    model: str
    embeddings: List[List[float]]


def normalize_embedding(values: Sequence[float]) -> List[float]:
    norm = sqrt(sum(v * v for v in values)) or 1.0
    return [v / norm for v in values]


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    a_norm = normalize_embedding(a)
    b_norm = normalize_embedding(b)
    return sum(x * y for x, y in zip(a_norm, b_norm))


def coerce_texts(texts: Iterable[str]) -> List[str]:
    return [str(t) for t in texts]
