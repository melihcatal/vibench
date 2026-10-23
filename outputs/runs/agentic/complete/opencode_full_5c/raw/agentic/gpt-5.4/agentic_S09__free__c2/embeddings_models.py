from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Sequence


@dataclass(slots=True)
class EmbeddingRequest:
    texts: list[str]
    model: str
    input_type: str = "search_document"
    truncate: str = "END"


@dataclass(slots=True)
class EmbeddingVector:
    index: int
    text: str
    embedding: list[float]


@dataclass(slots=True)
class EmbeddingResponse:
    model: str
    vectors: list[EmbeddingVector]
    id: str | None = None
    meta: dict[str, Any] | None = None


def normalize_text(value: str) -> str:
    return " ".join(value.split()).strip()


def normalize_texts(values: Sequence[str] | Iterable[str]) -> list[str]:
    normalized = [normalize_text(value) for value in values]
    return [value for value in normalized if value]


def parse_embedding_response(
    payload: dict[str, Any], texts: Sequence[str]
) -> EmbeddingResponse:
    items = payload.get("embeddings", [])
    vectors = [
        EmbeddingVector(
            index=index,
            text=texts[index] if index < len(texts) else "",
            embedding=[float(value) for value in item.get("embedding", [])],
        )
        for index, item in enumerate(items)
    ]
    return EmbeddingResponse(
        model=payload.get("model", "embed-english-v3.0"),
        vectors=vectors,
        id=payload.get("id"),
        meta=payload.get("meta"),
    )


def l2_normalize(vector: Sequence[float]) -> list[float]:
    magnitude = sum(component * component for component in vector) ** 0.5
    if magnitude == 0:
        return [0.0 for _ in vector]
    return [float(component) / magnitude for component in vector]
