import math
import os
from typing import List

from openai import OpenAI


def _embed(text: str, client: OpenAI, model: str = "text-embedding-3-small") -> List[float]:
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Embeddings must have the same length")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def similarity_score(text1: str, text2: str) -> float:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    emb1 = _embed(text1, client)
    emb2 = _embed(text2, client)
    return _cosine_similarity(emb1, emb2)
