from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any, Iterable, Sequence


@dataclass(slots=True)
class EmbeddingRequest:
    texts: list[str]
    model: str
    input_type: str | None = "search_document"
    truncate: str = "END"

    def as_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model,
            "texts": [normalize_text(text) for text in self.texts],
            "truncate": self.truncate,
        }
        if self.input_type:
            payload["input_type"] = self.input_type
        return payload


@dataclass(slots=True)
class EmbeddingVector:
    index: int
    text: str
    values: list[float]


@dataclass(slots=True)
class EmbeddingResponse:
    model: str
    embeddings: list[EmbeddingVector]
    response_id: str | None = None
    meta: dict[str, Any] | None = None


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def parse_embedding_response(
    payload: dict[str, Any], texts: Sequence[str]
) -> EmbeddingResponse:
    items = payload.get("embeddings", [])
    embeddings = [
        EmbeddingVector(
            index=index,
            text=texts[index] if index < len(texts) else "",
            values=[float(value) for value in item.get("embedding", [])],
        )
        for index, item in enumerate(items)
    ]
    return EmbeddingResponse(
        model=payload.get("model", "embed-v4.0"),
        embeddings=embeddings,
        response_id=payload.get("id"),
        meta=payload.get("meta"),
    )


def l2_normalize(vector: Sequence[float]) -> list[float]:
    magnitude = sqrt(sum(float(value) * float(value) for value in vector))
    if magnitude == 0:
        return [0.0 for _ in vector]
    return [float(value) / magnitude for value in vector]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    left_norm = l2_normalize(left)
    right_norm = l2_normalize(right)
    return sum(a * b for a, b in zip(left_norm, right_norm, strict=False))


def average_vector(vectors: Iterable[Sequence[float]]) -> list[float]:
    collected = [list(vector) for vector in vectors]
    if not collected:
        return []
    width = len(collected[0])
    totals = [0.0] * width
    for vector in collected:
        for index, value in enumerate(vector[:width]):
            totals[index] += float(value)
    return [value / len(collected) for value in totals]
