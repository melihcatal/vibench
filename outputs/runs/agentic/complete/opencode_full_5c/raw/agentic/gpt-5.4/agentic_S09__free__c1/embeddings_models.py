from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any


@dataclass(slots=True)
class EmbeddingRequest:
    texts: list[str]
    input_type: str = "search_document"
    truncate: str = "END"

    def to_payload(self, model: str) -> dict[str, Any]:
        return {
            "model": model,
            "texts": self.texts,
            "input_type": self.input_type,
            "truncate": self.truncate,
        }


@dataclass(slots=True)
class EmbeddingResponse:
    provider: str
    model: str
    embeddings: list[list[float]]
    meta: dict[str, Any]


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def normalize_texts(values: list[str]) -> list[str]:
    return [normalize_text(value) for value in values if normalize_text(value)]


def parse_cohere_embeddings(payload: dict[str, Any]) -> EmbeddingResponse:
    embeddings = payload.get("embeddings") or payload.get("float") or []
    response_type = payload.get("response_type")
    if isinstance(embeddings, dict):
        embeddings = embeddings.get("float") or []
    meta = payload.get("meta") or {}
    return EmbeddingResponse(
        provider="cohere",
        model=payload.get("id", "embed-v4.0"),
        embeddings=[[float(item) for item in vector] for vector in embeddings],
        meta={"response_type": response_type, **meta},
    )


def cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = sqrt(sum(a * a for a in left))
    right_norm = sqrt(sum(b * b for b in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return numerator / (left_norm * right_norm)
