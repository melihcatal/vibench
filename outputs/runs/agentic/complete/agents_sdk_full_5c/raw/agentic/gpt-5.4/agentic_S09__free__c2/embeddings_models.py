from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List, Sequence
import math


@dataclass(slots=True)
class EmbeddingRequest:
    input_text: str
    model: str = "text-embedding-3-small"


@dataclass(slots=True)
class BatchEmbeddingRequest:
    input_texts: List[str]
    model: str = "text-embedding-3-small"


@dataclass(slots=True)
class EmbeddingResult:
    index: int
    embedding: List[float]


@dataclass(slots=True)
class EmbeddingResponse:
    model: str
    data: List[EmbeddingResult]


@dataclass(slots=True)
class SearchEmbeddingBundle:
    query_embedding: List[float]
    document_embeddings: List[List[float]]


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def ensure_text_list(values: Iterable[str]) -> List[str]:
    items = [normalize_text(v) for v in values if normalize_text(v)]
    if not items:
        raise ValueError("At least one non-empty text is required")
    return items


def parse_embedding_response(payload: Any) -> EmbeddingResponse:
    model = getattr(payload, "model", None) or payload.get("model", "")
    raw_data = getattr(payload, "data", None) or payload.get("data", [])
    data = [
        EmbeddingResult(index=getattr(item, "index", item.get("index", idx)), embedding=list(getattr(item, "embedding", item.get("embedding", []))))
        for idx, item in enumerate(raw_data)
    ]
    return EmbeddingResponse(model=model, data=data)


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Embedding vectors must be the same length")
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        raise ValueError("Embedding vectors must be non-zero")
    return dot / (left_norm * right_norm)
