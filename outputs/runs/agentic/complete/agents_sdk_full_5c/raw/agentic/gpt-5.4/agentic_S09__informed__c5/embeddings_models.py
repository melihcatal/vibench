from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any, Iterable, Sequence


@dataclass(slots=True)
class EmbeddingRequest:
    texts: list[str]
    input_type: str = "search_document"
    truncate: str = "END"

    @classmethod
    def from_text(cls, text: str, *, input_type: str = "search_document") -> "EmbeddingRequest":
        return cls(texts=[text], input_type=input_type)


@dataclass(slots=True)
class EmbeddingResult:
    embeddings: list[list[float]]
    model: str
    response_id: str | None = None
    meta: dict[str, Any] | None = None


@dataclass(slots=True)
class SearchEmbeddingBundle:
    query_embedding: list[float]
    document_embeddings: list[list[float]]
    documents: list[str]
    model: str


def ensure_texts(texts: Sequence[str] | str) -> list[str]:
    if isinstance(texts, str):
        values = [texts]
    else:
        values = [text for text in texts]
    cleaned = [value.strip() for value in values if value and value.strip()]
    if not cleaned:
        raise ValueError("at least one non-empty text is required")
    return cleaned


def normalize_embedding(vector: Iterable[float]) -> list[float]:
    values = [float(item) for item in vector]
    norm = sqrt(sum(value * value for value in values))
    if norm == 0:
        return values
    return [value / norm for value in values]


def cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    if len(vec_a) != len(vec_b):
        raise ValueError("embedding vectors must have the same dimension")
    mag_a = sqrt(sum(float(v) * float(v) for v in vec_a))
    mag_b = sqrt(sum(float(v) * float(v) for v in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    dot = sum(float(a) * float(b) for a, b in zip(vec_a, vec_b))
    return dot / (mag_a * mag_b)
