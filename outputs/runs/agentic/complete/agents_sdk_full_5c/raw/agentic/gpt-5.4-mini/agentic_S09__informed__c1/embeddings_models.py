"""Local request/response and normalization helpers for OpenAI embeddings."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class EmbeddingRequest:
    input_texts: Sequence[str]
    model: str


@dataclass(frozen=True)
class EmbeddingResult:
    text: str
    embedding: List[float]


def normalize_vector(vector: Sequence[float]) -> List[float]:
    norm = sqrt(sum(value * value for value in vector))
    if norm == 0:
        return [0.0 for _ in vector]
    return [float(value / norm) for value in vector]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Vectors must have the same length.")
    left_n = normalize_vector(left)
    right_n = normalize_vector(right)
    return float(sum(l * r for l, r in zip(left_n, right_n)))


def ensure_texts(texts: Iterable[str]) -> List[str]:
    cleaned = [text.strip() for text in texts if text and text.strip()]
    if not cleaned:
        raise ValueError("At least one non-empty text is required.")
    return cleaned
