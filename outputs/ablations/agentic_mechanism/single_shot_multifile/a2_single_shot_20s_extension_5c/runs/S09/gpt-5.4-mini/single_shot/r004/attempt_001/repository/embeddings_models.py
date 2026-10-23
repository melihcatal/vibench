from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any, Iterable, List, Sequence


@dataclass
class EmbeddingRequest:
    model: str
    input: Any

    def to_payload(self) -> dict:
        return {"model": self.model, "input": self.input}


@dataclass
class NormalizedEmbeddingResponse:
    embedding: List[float] | None = None
    embeddings: List[List[float]] | None = None


def normalize_embedding_response(response: dict) -> NormalizedEmbeddingResponse:
    data = response.get("data", [])
    vectors = [item["embedding"] for item in sorted(data, key=lambda item: item.get("index", 0))]
    if len(vectors) == 1:
        return NormalizedEmbeddingResponse(embedding=vectors[0], embeddings=vectors)
    return NormalizedEmbeddingResponse(embedding=vectors[0] if vectors else None, embeddings=vectors)


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sqrt(sum(x * x for x in a))
    norm_b = sqrt(sum(y * y for y in b))
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)
