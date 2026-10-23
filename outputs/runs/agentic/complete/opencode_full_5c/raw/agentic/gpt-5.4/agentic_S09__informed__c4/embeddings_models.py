from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any, Iterable, Sequence


@dataclass(slots=True)
class EmbeddingRequest:
    texts: list[str]
    model: str
    input_type: str = "search_document"
    truncate: str = "END"


@dataclass(slots=True)
class EmbeddingResult:
    index: int
    text: str
    embedding: list[float]


@dataclass(slots=True)
class EmbeddingResponse:
    model: str
    results: list[EmbeddingResult]
    meta: dict[str, Any]


def ensure_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_texts(values: Iterable[Any]) -> list[str]:
    normalized = [ensure_text(value) for value in values]
    return [value for value in normalized if value]


def parse_cohere_embeddings(
    payload: dict[str, Any], texts: Sequence[str]
) -> EmbeddingResponse:
    embeddings = payload.get("embeddings") or payload.get("data") or []
    results = [
        EmbeddingResult(
            index=index, text=texts[index], embedding=[float(v) for v in vector]
        )
        for index, vector in enumerate(embeddings)
    ]
    return EmbeddingResponse(
        model=str(payload.get("id") or payload.get("response_type") or "embed-v4.0"),
        results=results,
        meta=dict(payload.get("meta") or {}),
    )


def l2_normalize(vector: Sequence[float]) -> list[float]:
    magnitude = sqrt(sum(float(value) * float(value) for value in vector))
    if magnitude == 0:
        return [0.0 for _ in vector]
    return [float(value) / magnitude for value in vector]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Embedding vectors must have the same dimensionality")
    left_norm = l2_normalize(left)
    right_norm = l2_normalize(right)
    return sum(l * r for l, r in zip(left_norm, right_norm))
