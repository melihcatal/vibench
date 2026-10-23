from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt
from typing import Any, Iterable, Sequence


@dataclass(slots=True)
class EmbeddingRequest:
    text: str
    model: str = "text-embedding-3-small"

    def normalized_text(self) -> str:
        return normalize_text(self.text)


@dataclass(slots=True)
class BatchEmbeddingRequest:
    texts: list[str]
    model: str = "text-embedding-3-small"

    def normalized_inputs(self) -> list[str]:
        return [normalize_text(text) for text in self.texts]


@dataclass(slots=True)
class EmbeddingResult:
    index: int
    vector: list[float] = field(default_factory=list)
    source_text: str = ""


@dataclass(slots=True)
class SearchEmbeddingBundle:
    query_vector: list[float]
    document_vectors: list[list[float]]
    documents: list[str]
    model: str


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def ensure_texts(texts: Iterable[str]) -> list[str]:
    normalized = [normalize_text(text) for text in texts if normalize_text(text)]
    if not normalized:
        raise ValueError("At least one non-empty text value is required.")
    return normalized


def parse_embedding_response_item(item: dict[str, Any], source_text: str = "") -> EmbeddingResult:
    return EmbeddingResult(
        index=int(item.get("index", 0)),
        vector=[float(value) for value in item.get("embedding", [])],
        source_text=source_text,
    )


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Embedding vectors must have the same dimensionality.")
    if not left:
        raise ValueError("Embedding vectors cannot be empty.")
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = sqrt(sum(a * a for a in left))
    right_norm = sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        raise ValueError("Embedding vectors must be non-zero.")
    return dot / (left_norm * right_norm)
