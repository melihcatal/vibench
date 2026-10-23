from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any, Iterable, Sequence


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass(slots=True)
class EmbeddingRequest:
    texts: list[str]
    model: str = DEFAULT_EMBEDDING_MODEL


@dataclass(slots=True)
class EmbeddingItem:
    index: int
    embedding: list[float]


@dataclass(slots=True)
class EmbeddingResponse:
    model: str
    items: list[EmbeddingItem]
    usage: dict[str, Any]


def normalize_text(value: str) -> str:
    return " ".join(value.split())


def normalize_texts(values: Sequence[str]) -> list[str]:
    return [normalize_text(value) for value in values]


def parse_embedding_response(response: Any) -> EmbeddingResponse:
    items = [
        EmbeddingItem(index=item.index, embedding=list(item.embedding))
        for item in response.data
    ]
    usage = {}
    if getattr(response, "usage", None) is not None:
        usage = dict(response.usage.model_dump())
    return EmbeddingResponse(model=response.model, items=items, usage=usage)


def cosine_similarity(left: Iterable[float], right: Iterable[float]) -> float:
    left_list = list(left)
    right_list = list(right)
    dot = sum(a * b for a, b in zip(left_list, right_list))
    left_norm = sqrt(sum(a * a for a in left_list))
    right_norm = sqrt(sum(b * b for b in right_list))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (left_norm * right_norm)
