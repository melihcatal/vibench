from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass(slots=True)
class EmbeddingRequest:
    input: str | list[str]
    model: str = DEFAULT_EMBEDDING_MODEL
    dimensions: int | None = None
    user: str | None = None

    def to_openai_kwargs(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model,
            "input": self.input,
        }
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        if self.user:
            payload["user"] = self.user
        return payload


@dataclass(slots=True)
class EmbeddingVector:
    index: int
    embedding: list[float]


@dataclass(slots=True)
class EmbeddingResponse:
    model: str
    vectors: list[EmbeddingVector] = field(default_factory=list)
    usage: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_openai_response(cls, response: Any) -> "EmbeddingResponse":
        vectors = [
            EmbeddingVector(index=item.index, embedding=list(item.embedding))
            for item in response.data
        ]
        usage = {}
        if getattr(response, "usage", None) is not None:
            usage = {
                "prompt_tokens": getattr(response.usage, "prompt_tokens", None),
                "total_tokens": getattr(response.usage, "total_tokens", None),
            }
        return cls(model=response.model, vectors=vectors, usage=usage)


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def normalize_texts(texts: Iterable[str]) -> list[str]:
    return [normalize_text(text) for text in texts]


def l2_norm(vector: Sequence[float]) -> float:
    return sum(value * value for value in vector) ** 0.5


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Vectors must have the same dimensionality")
    left_norm = l2_norm(left)
    right_norm = l2_norm(right)
    if left_norm == 0 or right_norm == 0:
        raise ValueError("Vectors must be non-zero for cosine similarity")
    dot = sum(a * b for a, b in zip(left, right))
    return dot / (left_norm * right_norm)
