from __future__ import annotations

from collections.abc import Sequence


def normalize_single_text_input(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("text cannot be empty")
    return cleaned


def normalize_batch_text_input(texts: Sequence[str]) -> list[str]:
    if not isinstance(texts, Sequence):
        raise TypeError("texts must be a sequence of strings")
    normalized = [normalize_single_text_input(text) for text in texts]
    if not normalized:
        raise ValueError("texts cannot be empty")
    return normalized


def normalize_embedding_response(response) -> list[list[float]]:
    data = getattr(response, "data", None)
    if data is None:
        raise ValueError("invalid embedding response")
    vectors: list[list[float]] = []
    for item in data:
        embedding = getattr(item, "embedding", None)
        if embedding is None:
            raise ValueError("invalid embedding item")
        vectors.append([float(value) for value in embedding])
    if not vectors:
        raise ValueError("empty embedding response")
    return vectors
