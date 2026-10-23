import os
from typing import List


def _openai_embedding(text: str) -> List[float]:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return list(response.data[0].embedding)


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Embedding vectors must have the same dimension")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    if norm_a == 0.0 or norm_b == 0.0:
        raise ValueError("Embedding vectors must be non-zero")
    return dot / (norm_a * norm_b)


def similarity_score(text_a: str, text_b: str) -> float:
    emb_a = _openai_embedding(text_a)
    emb_b = _openai_embedding(text_b)
    return _cosine_similarity(emb_a, emb_b)
