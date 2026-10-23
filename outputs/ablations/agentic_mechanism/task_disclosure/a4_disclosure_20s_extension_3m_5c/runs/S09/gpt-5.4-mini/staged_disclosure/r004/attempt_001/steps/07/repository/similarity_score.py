import os
import math
import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _embed(text: str) -> list[float]:
    api_key = os.environ["OPENAI_API_KEY"]
    response = requests.post(
        OPENAI_EMBEDDINGS_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": OPENAI_EMBEDDING_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["data"][0]["embedding"]


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def similarity_score(text1: str, text2: str) -> float:
    return _cosine_similarity(_embed(text1), _embed(text2))
