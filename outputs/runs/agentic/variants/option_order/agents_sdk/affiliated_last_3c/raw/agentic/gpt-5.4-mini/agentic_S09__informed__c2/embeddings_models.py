from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class EmbeddingRequest:
    text: str


@dataclass
class EmbeddingBatchRequest:
    texts: List[str]


@dataclass
class EmbeddingResponse:
    vector: List[float]
    model: str


@dataclass
class EmbeddingBatchResponse:
    vectors: List[List[float]]
    model: str


def normalize_text(value: str) -> str:
    return " ".join((value or "").strip().split())


def normalize_texts(values: Iterable[str]) -> List[str]:
    return [normalize_text(v) for v in values if normalize_text(v)]


def cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        raise ValueError("Embedding vectors must be non-empty and the same length")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    if norm_a == 0.0 or norm_b == 0.0:
        raise ValueError("Embedding vectors must not be zero vectors")
    return dot / (norm_a * norm_b)
