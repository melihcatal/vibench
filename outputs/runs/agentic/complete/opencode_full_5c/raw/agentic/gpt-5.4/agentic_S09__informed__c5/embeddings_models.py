from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any, Iterable, Sequence


@dataclass(slots=True)
class EmbeddingRequest:
    texts: list[str]
    input_type: str = "search_document"
    model: str = "embed-english-v3.0"


@dataclass(slots=True)
class EmbeddingResponse:
    embeddings: list[list[float]]
    model: str
    provider: str = "cohere"


def ensure_text(value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError("text must be a non-empty string")
    return normalized


def ensure_texts(values: Sequence[str]) -> list[str]:
    texts = [ensure_text(value) for value in values]
    if not texts:
        raise ValueError("at least one text is required")
    return texts


def vector_from_iterable(values: Iterable[Any]) -> list[float]:
    return [float(value) for value in values]


def normalize_embedding_response(result: Any, model: str) -> EmbeddingResponse:
    embeddings = [vector_from_iterable(vector) for vector in result.embeddings]
    return EmbeddingResponse(embeddings=embeddings, model=model)


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("embedding dimensions must match")
    left_norm = sqrt(sum(value * value for value in left))
    right_norm = sqrt(sum(value * value for value in right))
    if left_norm == 0.0 or right_norm == 0.0:
        raise ValueError("embeddings must be non-zero vectors")
    dot = sum(l * r for l, r in zip(left, right))
    return dot / (left_norm * right_norm)
