from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence


@dataclass(slots=True)
class EmbeddingRequest:
    texts: list[str]
    model: str = "text-embedding-3-small"
    dimensions: int | None = None

    @classmethod
    def from_text(cls, text: str, model: str = "text-embedding-3-small", dimensions: int | None = None) -> "EmbeddingRequest":
        return cls(texts=[text], model=model, dimensions=dimensions)

    @classmethod
    def from_iterable(
        cls,
        texts: Iterable[str],
        model: str = "text-embedding-3-small",
        dimensions: int | None = None,
    ) -> "EmbeddingRequest":
        normalized = [normalize_text(text) for text in texts if normalize_text(text)]
        return cls(texts=normalized, model=model, dimensions=dimensions)


@dataclass(slots=True)
class EmbeddingVector:
    index: int
    embedding: list[float]
    source_text: str | None = None


@dataclass(slots=True)
class EmbeddingResponse:
    model: str
    vectors: list[EmbeddingVector] = field(default_factory=list)
    usage: dict[str, Any] = field(default_factory=dict)

    @property
    def embeddings(self) -> list[list[float]]:
        return [item.embedding for item in self.vectors]



def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())



def normalize_texts(texts: Iterable[str]) -> list[str]:
    return [value for value in (normalize_text(text) for text in texts) if value]



def l2_normalize(vector: Sequence[float]) -> list[float]:
    magnitude = sum(component * component for component in vector) ** 0.5
    if magnitude == 0:
        return [0.0 for _ in vector]
    return [component / magnitude for component in vector]



def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Vectors must have equal dimensions")
    left_norm = l2_normalize(left)
    right_norm = l2_normalize(right)
    return sum(l * r for l, r in zip(left_norm, right_norm))
