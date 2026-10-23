from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Mapping, Sequence
import math


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass(slots=True)
class EmbeddingRequest:
    texts: Sequence[str]
    model: str = OPENAI_EMBEDDING_MODEL
    dimensions: int | None = None

    def normalized_inputs(self) -> list[str]:
        normalized: list[str] = []
        for text in self.texts:
            if text is None:
                continue
            value = str(text).strip()
            if value:
                normalized.append(value)
        return normalized


@dataclass(slots=True)
class EmbeddingVector:
    index: int
    embedding: list[float]


@dataclass(slots=True)
class EmbeddingResponse:
    model: str
    vectors: list[EmbeddingVector] = field(default_factory=list)
    usage: Mapping[str, Any] | None = None


@dataclass(slots=True)
class SearchEmbeddingBundle:
    query: list[float]
    documents: list[list[float]]
    model: str


def parse_openai_embedding_response(response: Any) -> EmbeddingResponse:
    usage = getattr(response, "usage", None)
    usage_dict = None
    if usage is not None:
        usage_dict = {
            key: getattr(usage, key)
            for key in dir(usage)
            if not key.startswith("_") and not callable(getattr(usage, key))
        }
    vectors = [
        EmbeddingVector(index=item.index, embedding=list(item.embedding))
        for item in response.data
    ]
    return EmbeddingResponse(model=response.model, vectors=vectors, usage=usage_dict)


def l2_normalize(vector: Iterable[float]) -> list[float]:
    values = [float(v) for v in vector]
    norm = math.sqrt(sum(v * v for v in values))
    if norm == 0.0:
        return values
    return [v / norm for v in values]


def cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimensionality")
    norm_a = l2_normalize(vec_a)
    norm_b = l2_normalize(vec_b)
    return sum(a * b for a, b in zip(norm_a, norm_b))
