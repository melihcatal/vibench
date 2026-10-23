import math
import os
from typing import List

import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        raise ValueError("Vectors must be non-zero")
    return dot / (norm_a * norm_b)


def _embed_text(text: str) -> List[float]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_EMBEDDINGS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_EMBEDDING_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["data"][0]["embedding"]


def similarity_score(text_a: str, text_b: str) -> float:
    embedding_a = _embed_text(text_a)
    embedding_b = _embed_text(text_b)
    return _cosine_similarity(embedding_a, embedding_b)
