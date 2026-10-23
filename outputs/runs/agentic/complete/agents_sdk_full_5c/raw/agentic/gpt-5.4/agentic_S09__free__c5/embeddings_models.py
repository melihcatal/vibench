from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any, Iterable, Sequence


@dataclass(slots=True)
class EmbeddingRequest:
    input: str | list[str]
    model: str = "text-embedding-3-small"
    dimensions: int | None = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "input": self.input,
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
    data: list[EmbeddingResult]
    usage: dict[str, Any]

    @classmethod
    def from_openai_response(cls, response: Any) -> "EmbeddingResponse":
        model = getattr(response, "model", "text-embedding-3-small")
        usage_obj = getattr(response, "usage", None)
        usage = getattr(usage_obj, "__dict__", usage_obj) or {}
        data = [
            EmbeddingResult(index=item.index, embedding=list(item.embedding))
            for item in response.data
        ]
        return cls(model=model, data=data, usage=dict(usage))


def l2_normalize(vector: Sequence[float]) -> list[float]:
    norm = sqrt(sum(component * component for component in vector))
    if norm == 0:
        return [0.0 for _ in vector]
    return [component / norm for component in vector]


def cosine_similarity(vector_a: Sequence[float], vector_b: Sequence[float]) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have equal dimensions")
    numerator = sum(a * b for a, b in zip(vector_a, vector_b))
    denominator_a = sqrt(sum(a * a for a in vector_a))
    denominator_b = sqrt(sum(b * b for b in vector_b))
    if denominator_a == 0 or denominator_b == 0:
        return 0.0
    return numerator / (denominator_a * denominator_b)


def ensure_text_list(value: str | Iterable[str]) -> list[str]:
    if isinstance(value, str):
        return [value]
    return [item for item in value]
