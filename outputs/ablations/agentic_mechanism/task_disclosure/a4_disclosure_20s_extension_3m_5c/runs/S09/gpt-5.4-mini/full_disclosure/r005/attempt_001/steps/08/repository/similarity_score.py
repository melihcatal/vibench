import math
import os
from typing import Iterable, Sequence

import requests


OPENAI_EMBEDDINGS_API_HOST = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDINGS_MODEL = os.getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small")


def _vector_from_openai(text: str) -> list[float]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_EMBEDDINGS_API_HOST,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": OPENAI_EMBEDDINGS_MODEL, "input": text},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["data"][0]["embedding"]


def _cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Embedding vectors must have the same length")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        raise ValueError("Embedding vectors must be non-zero")
    return dot / (norm_a * norm_b)


def similarity_score(text_a: str, text_b: str) -> float:
    embedding_a = _vector_from_openai(text_a)
    embedding_b = _vector_from_openai(text_b)
    return _cosine_similarity(embedding_a, embedding_b)
