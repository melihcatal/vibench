from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any, Iterable, Sequence


def normalize_input_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_input_texts(texts: Sequence[str]) -> list[str]:
    return [normalize_input_text(text) for text in texts if normalize_input_text(text)]


def l2_normalize(vector: Sequence[float]) -> list[float]:
    magnitude = sqrt(sum(value * value for value in vector))
    if magnitude == 0:
        return [0.0 for _ in vector]
    return [value / magnitude for value in vector]


def cosine_similarity(vector_a: Sequence[float], vector_b: Sequence[float]) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have the same dimensionality")
    norm_a = sqrt(sum(value * value for value in vector_a))
    norm_b = sqrt(sum(value * value for value in vector_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    dot = sum(left * right for left, right in zip(vector_a, vector_b))
    return dot / (norm_a * norm_b)


@dataclass(slots=True)
class EmbeddingRecord:
    index: int
    embedding: list[float]


@dataclass(slots=True)
class EmbeddingResult:
    model: str
    provider: str
    records: list[EmbeddingRecord]
    usage: dict[str, Any]

    def first_vector(self) -> list[float]:
        if not self.records:
            raise ValueError("No embeddings returned")
        return self.records[0].embedding


def parse_embedding_response(payload: dict[str, Any]) -> EmbeddingResult:
    records = [
        EmbeddingRecord(index=item["index"], embedding=list(item["embedding"]))
        for item in payload.get("data", [])
    ]
    return EmbeddingResult(
        model=payload.get("model", "text-embedding-3-small"),
        provider="openai",
        records=records,
        usage=dict(payload.get("usage", {})),
    )


def summarize_vector_dimensions(vectors: Iterable[Sequence[float]]) -> dict[str, int]:
    lengths = [len(vector) for vector in vectors]
    return {
        "count": len(lengths),
        "dimensions": lengths[0] if lengths else 0,
    }
