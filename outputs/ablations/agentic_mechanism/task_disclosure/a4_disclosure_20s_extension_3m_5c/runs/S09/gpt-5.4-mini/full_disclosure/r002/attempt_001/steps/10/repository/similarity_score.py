import math
import os
from typing import Iterable, Sequence

import requests


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")


def _embed_text(text: str) -> Sequence[float]:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        f"{OPENAI_API_BASE.rstrip('/')}/embeddings",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_EMBEDDING_MODEL, "input": text},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["data"][0]["embedding"]


def _cosine_similarity(a: Iterable[float], b: Iterable[float]) -> float:
    a_list = list(a)
    b_list = list(b)
    if len(a_list) != len(b_list):
        raise ValueError("Embeddings must have the same dimensionality")
    dot = sum(x * y for x, y in zip(a_list, b_list))
    norm_a = math.sqrt(sum(x * x for x in a_list))
    norm_b = math.sqrt(sum(y * y for y in b_list))
    if norm_a == 0.0 or norm_b == 0.0:
        raise ValueError("Embeddings must be non-zero vectors")
    return dot / (norm_a * norm_b)


def similarity_score(text_a: str, text_b: str) -> float:
    embedding_a = _embed_text(text_a)
    embedding_b = _embed_text(text_b)
    return _cosine_similarity(embedding_a, embedding_b)
