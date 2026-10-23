from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any, Iterable


@dataclass(slots=True)
class EmbeddingRequest:
    model: str
    input: str | list[str]
    dimensions: int | None = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"model": self.model, "input": self.input}
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        return payload


@dataclass(slots=True)
class EmbeddingVector:
    index: int
    embedding: list[float]


@dataclass(slots=True)
class EmbeddingResponse:
    model: str
    provider: str
    vectors: list[EmbeddingVector]
    usage: dict[str, Any]


def normalize_text(value: str) -> str:
    return " ".join(value.split())


def normalize_texts(values: Iterable[str]) -> list[str]:
    return [normalize_text(value) for value in values]


def parse_embedding_response(
    data: dict[str, Any], provider: str = "OpenAI"
) -> EmbeddingResponse:
    vectors = [
        EmbeddingVector(
            index=item["index"], embedding=[float(x) for x in item["embedding"]]
        )
        for item in data.get("data", [])
    ]
    return EmbeddingResponse(
        model=data.get("model", "text-embedding-3-small"),
        provider=provider,
        vectors=vectors,
        usage=data.get("usage", {}),
    )


def cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = sqrt(sum(a * a for a in left))
    right_norm = sqrt(sum(b * b for b in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return numerator / (left_norm * right_norm)
