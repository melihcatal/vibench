from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt
from typing import Any, Iterable, Sequence


@dataclass(slots=True)
class EmbeddingRequest:
    text: str
    model: str = "text-embedding-3-small"
    dimensions: int | None = None

    def normalized_text(self) -> str:
        return normalize_text(self.text)

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "input": self.normalized_text(),
            "model": self.model,
        }
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        return payload


@dataclass(slots=True)
class BatchEmbeddingRequest:
    texts: list[str]
    model: str = "text-embedding-3-small"
    dimensions: int | None = None

    def normalized_inputs(self) -> list[str]:
        return [normalize_text(text) for text in self.texts]

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "input": self.normalized_inputs(),
            "model": self.model,
        }
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        return payload


@dataclass(slots=True)
class EmbeddingResult:
    index: int
    embedding: list[float]


@dataclass(slots=True)
class EmbeddingResponse:
    model: str
    data: list[EmbeddingResult] = field(default_factory=list)
    usage: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_openai_dict(cls, payload: dict[str, Any]) -> "EmbeddingResponse":
        items = [
            EmbeddingResult(index=item["index"], embedding=list(item["embedding"]))
            for item in payload.get("data", [])
        ]
        return cls(model=payload.get("model", ""), data=items, usage=payload.get("usage", {}))


@dataclass(slots=True)
class SearchEmbeddingBundle:
    query_embedding: list[float]
    document_embeddings: list[list[float]]


def normalize_text(text: str) -> str:
    collapsed = " ".join(text.split())
    return collapsed.strip()


def l2_normalize(vector: Sequence[float]) -> list[float]:
    magnitude = sqrt(sum(value * value for value in vector))
    if magnitude == 0:
        return [0.0 for _ in vector]
    return [value / magnitude for value in vector]


def cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimensionality.")
    norm_a = l2_normalize(vec_a)
    norm_b = l2_normalize(vec_b)
    return sum(a * b for a, b in zip(norm_a, norm_b))


def mean_pool(vectors: Iterable[Sequence[float]]) -> list[float]:
    vectors = list(vectors)
    if not vectors:
        return []
    size = len(vectors[0])
    if any(len(vector) != size for vector in vectors):
        raise ValueError("All vectors must share the same dimensionality.")
    return [sum(vector[i] for vector in vectors) / len(vectors) for i in range(size)]
