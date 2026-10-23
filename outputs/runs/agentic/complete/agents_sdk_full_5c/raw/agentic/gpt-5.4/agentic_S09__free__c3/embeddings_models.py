from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List, Sequence
import math


@dataclass(slots=True)
class EmbeddingRequest:
    text: str
    model: str = "text-embedding-3-small"


@dataclass(slots=True)
class BatchEmbeddingRequest:
    texts: Sequence[str]
    model: str = "text-embedding-3-small"


@dataclass(slots=True)
class EmbeddingResult:
    model: str
    vectors: List[List[float]]
    usage: dict[str, Any] | None = None


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_texts(texts: Iterable[str]) -> List[str]:
    return [normalize_text(text) for text in texts if normalize_text(text)]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Embedding vectors must have identical dimensions")
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        raise ValueError("Embedding vectors must be non-zero")
    return sum(a * b for a, b in zip(left, right)) / (left_norm * right_norm)


def summarize_embedding_lengths(vectors: Sequence[Sequence[float]]) -> dict[str, float]:
    lengths = [len(vector) for vector in vectors]
    if not lengths:
        return {"count": 0, "min": 0, "max": 0, "avg": 0.0}
    return {
        "count": len(lengths),
        "min": min(lengths),
        "max": max(lengths),
        "avg": sum(lengths) / len(lengths),
    }
