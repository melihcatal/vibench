from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Sequence


@dataclass(slots=True)
class EmbeddingRequest:
    texts: List[str]
    model: str = "text-embedding-3-small"
    input_type: str = "search_document"

    @classmethod
    def from_text(cls, text: str, model: str = "text-embedding-3-small", input_type: str = "search_document") -> "EmbeddingRequest":
        return cls(texts=[normalize_text(text)], model=model, input_type=input_type)

    @classmethod
    def from_texts(
        cls,
        texts: Sequence[str],
        model: str = "text-embedding-3-small",
        input_type: str = "search_document",
    ) -> "EmbeddingRequest":
        return cls(texts=[normalize_text(text) for text in texts], model=model, input_type=input_type)


@dataclass(slots=True)
class EmbeddingRecord:
    index: int
    embedding: List[float]
    text: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EmbeddingResponse:
    model: str
    records: List[EmbeddingRecord]
    provider: str = "openai"
    usage: dict[str, Any] = field(default_factory=dict)

    def vectors(self) -> List[List[float]]:
        return [record.embedding for record in self.records]


@dataclass(slots=True)
class SearchEmbeddingSet:
    query: EmbeddingRecord
    documents: List[EmbeddingRecord]
    model: str


@dataclass(slots=True)
class SimilarityResult:
    score: float
    left_model: str
    right_model: str
    provider: str = "openai"


def normalize_text(text: str) -> str:
    return " ".join(str(text).split())


def normalize_texts(texts: Iterable[str]) -> List[str]:
    return [normalize_text(text) for text in texts]


def l2_norm(vector: Sequence[float]) -> float:
    return sum(value * value for value in vector) ** 0.5


def normalize_vector(vector: Sequence[float]) -> List[float]:
    norm = l2_norm(vector)
    if norm == 0:
        return [0.0 for _ in vector]
    return [float(value) / norm for value in vector]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    left_norm = normalize_vector(left)
    right_norm = normalize_vector(right)
    return float(sum(a * b for a, b in zip(left_norm, right_norm)))
